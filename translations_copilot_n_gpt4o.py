code_snippet = """
const centiroFetch = async (path, body, requestId, version, retailId, zipCode) => {
  const url = Config.config.feature.enableDSM
    ? buildUrlDSM(path, retailId)
    : `${Config.config.centiro.endpoint}/${path}`;
  const headers = {
    'Content-Type': 'application/json',
    Accept: `application/vnd.centiro+json;version=v${version}`,
  };
  const response = await soFetcherObject
    .soFetcher({
      url,
      payload: {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      },
      system: 'centiro',
      requestId,
      retailId,
    })
    .catch(async (fetch) => {
      if (typeof fetch?.response?.json !== 'function') {
        if (!fetch) {
          console.log('Fetch is undefined');
        } else if (!fetch.response) {
          console.log('response is missing', JSON.stringify(fetch));
        } else if (typeof fetch.response.clone !== 'function') {
          console.log('clone is not a function, have a json!', JSON.stringify(fetch));
        }
        throw new ConnectionError(ErrorCauses.CENTIRO_CONNECTION_PROBLEM, {
          statusCode: 500,
          errorDescription: 'Unable to retrieve proper response from Centiro, time out',
          requestId,
          retailId,
          log: {
            system: 'centiro',
            url,
            payload: body,
            response: await fetch?.response?.clone().text(),
            centiroConnectionError: true,
          },
        });
      }
      await fetch.response
        .clone()
        .json()
        .catch(async (jsonParseError) => {
          throw new ConnectionError(ErrorCauses.CENTIRO_CONNECTION_PROBLEM, {
            statusCode: 500,
            errorDescription: 'Unable to retrieve proper response from Centiro, did not receive JSON response',
            requestId,
            retailId,
            log: {
              system: 'centiro',
              url,
              payload: body,
              jsonParseError,
              response: await fetch?.response?.clone().text(),
              centiroConnectionError: true,
            },
          });
        })
        .then((responseJSON) => {
          const errorCode =
            responseJSON?.error?.errorCode ||
            responseJSON?.getServiceDateProposalResponse?.proposedServiceTypes.find((proposedServiceType) =>
              proposedServiceType.serviceLines.find((serviceLine) => serviceLine?.error?.errorCode),
            )?.serviceLines[0].error.errorCode;
          const errorMessage = responseJSON?.error?.errorDescription;
          if (invalidServiceCode === errorCode) {
            throw new ServiceCodeError(ErrorCauses.SERVICECODE_NOT_MATCHED, {
              errorCode: 422,
              field: ['services[].serviceCode'],
              requestId,
              retailId,
            });
          }
          if (Object.keys(localityErrorCode).includes(errorCode)) {
            throw new LocalityError(ErrorCauses.LOCALITY_NOT_DEFINED, {
              statusCode: 422,
              value: [retailId, zipCode],
              errorDescription: 'The provided retail ID and/or locality combination is not available',
              field: localityErrorCode[errorCode],
              requestId,
              logAsInfo: true,
              retailId,
            });
          }
          if (zipCodeErrorCode === errorCode) {
            throw new ZipCodeError(ErrorCauses.LOCALITY_NOT_DEFINED, {
              errorCode: 422,
              field: ['zipCode'],
              requestId,
              logAsInfo: true,
              retailId,
            });
          }
          if (buErrorCode === errorCode) {
            throw new BuError(ErrorCauses.BU_NOT_DEFINED_CENTIRO, {
              statusCode: 422,
              field: ['businessUnit.buCode', 'businessUnit.buType'],
              requestId,
              retailId,
            });
          }
          if (Object.keys(inputErrorCode).includes(errorCode)) {
            throw new InputError(ErrorCauses.INPUT_INVALID_BY_CENTIRO, {
              statusCode: 422,
              field: inputErrorCode[errorCode],
              requestId,
              retailId,
            });
          }
          if (invalidRequestErrorCode === errorCode && errorMessage) {
            const errorField = Object.keys(invalidRequestKeyword).find((keyword) =>
              errorMessage.match(`.*${keyword}.*`),
            );
            throw new InputError(ErrorCauses.INPUT_INVALID_BY_CENTIRO, {
              statusCode: 422,
              ...(errorField && {
                field: invalidRequestKeyword[errorField],
                errorDescription: `Validation failed. Centiro was unable to parse the field ${invalidRequestKeyword[errorField]}`,
              }),
              ...(!errorField && {
                downstreamErrorMessage: errorMessage,
              }),
              requestId,
              logAsInfo: true,
              retailId,
            });
          }
          if (noAvailableSlotsCode.includes(errorCode)) {
            throw new CapacityError(ErrorCauses.SERVICE_TIME_WINDOW_FOR_START_DATE, {
              statusCode: 404,
              value: [retailId, zipCode],
              errorDescription:
                'No service time windows with capacity could be found after the provided start date from Centiro',
              requestId,
              retailId,
              logAsInfo: true,
            });
          }
          if (ErrorCodes.NO_SERVICE_PROVIDER_AVAILABLE === errorCode) {
            throw new ServiceProviderError(ErrorCauses.NO_SERVICE_PROVIDER_AVAILABLE, {
              statusCode: 422,
              value: [retailId, zipCode],
              errorDescription: ErrorMessages.NO_SERVICE_PROVIDER_AVAILABLE,
              requestId,
              retailId,
              logAsInfo: true,
            });
          }
          if (connectionErrorCode.includes(errorCode)) {
            throw new ConnectionError(ErrorCauses.CENTIRO_CONNECTION_PROBLEM, {
              statusCode: 500,
              errorDescription: `Centiro response failed with ${errorCode}`,
              requestId,
              retailId,
              log: {
                system: 'centiro',
                response: responseJSON,
                url,
              },
            });
          }
          throw new ConnectionError(ErrorCauses.CENTIRO_CONNECTION_PROBLEM, {
            statusCode: 500,
            errorDescription: 'Unable to retrieve proper response from Centiro',
            requestId,
            retailId,
            log: {
              system: 'centiro',
              response: responseJSON,
              url,
              payload: JSON.stringify(body),
              requestId,
            },
          });
        });
    });

  return response
    ?.json()
    .then((responseJSON) => responseJSON)
    .catch(() => {
      if (response.status === 204) return {};
      throw new ConnectionError(ErrorCauses.CENTIRO_CONNECTION_PROBLEM, {
        statusCode: response.status,
        errorDescription: 'Unable to retrieve proper response from Centiro, did not receive JSON response',
        requestId,
        retailId,
        log: {
          system: 'centiro',
          url,
          payload: JSON.stringify(body),
        },
      });
    });
};
"""
code_snippet1 = """
export function purgeData(item, endpoint: string): Maybe<Item> {
  let newItem: Maybe<Item>;
  if (endpoint === 'communications') {
    newItem = {
      itemKey: {
        itemNo: item.itemKey.itemNo,
        itemType: item.itemKey.itemType,
      },
      productNameGlobal: item.productNameGlobal,
      isAssemblyRequired: item?.isAssemblyRequired ?? undefined,
      professionalAssemblyTime: item.professionalAssemblyTime,
      numberOfPackages: item?.numberOfPackages ?? 0,
      businessStructure: item?.businessStructure ?? undefined,
      ...(item.childItems?.length && {
        childItems: item.childItems?.map((childItem) => ({
          ...(childItem.itemKey && {
            itemNo: childItem.itemKey.itemNo,
          }),
        })),
      }),
      ...(item.serviceProductRelations?.length && {
        serviceProductRelations: item.serviceProductRelations
          ?.filter((service) => isValidServiceById(service.serviceKey.itemNo))
          .map((relation) => ({
            serviceKey: {
              itemNo: relation.serviceKey.itemNo,
            },
            isCoWorkerAssistanceNeeded: relation.isCoWorkerAssistanceNeeded,
          })),
      }),
    };
    // below method retains the required fields needed from localizedCommunications, as it was making this fnc bigger , its chunked out as separte function
    newItem.localisedCommunications = mapLocalizedCommunicationItem(item);
  }

  if (endpoint === 'salesprices') {
    newItem = {
      itemKey: {
        itemNo: item.itemKey.itemNo,
        itemType: item.itemKey.itemType,
      },
      ...(item.servicePrices?.length && {
        servicePrices: item.servicePrices
          ?.filter((service) => isValidServiceByType(service.serviceProductId))
          .map((price) => ({
            serviceProductId: price.serviceProductId,
            priceInclTax: price.priceInclTax,
            priceExclTax: price.priceExclTax,
            indicativeTotalTax: price.indicativeTotalTax,
          })),
      }),
    };
  }

  return newItem;
}
"""


copilot_translation = """
Function Name: centiroFetch
📌 Description:
This function is responsible for fetching data from the Centiro API. It constructs the URL for the API call based on the configuration, sets the necessary headers, and sends a POST request with the provided body. The function handles various error scenarios and throws appropriate custom errors based on the response from the Centiro service. This function is crucial for the application as it interacts with the Centiro API, which is a key external service.

📥 Parameters:

path (String): The endpoint path for the API call.
body (Object): The body of the POST request.
requestId (String): The unique identifier for the request.
version (String): The version of the API to use.
retailId (String): The identifier for the retail store.
zipCode (String): The zip code for the request.
📤 Returns:

(Promise<Object>): Returns a promise that resolves to the JSON response from the Centiro service. If the response status is 204, it returns an empty object. If an error occurs, it throws a custom error with detailed information.
🔗 External Dependencies:

soFetcherObject.soFetcher: A function used to send the HTTP request.
Config.config: Configuration object used to determine the URL and other settings.
buildUrlDSM: A function used to build the URL for DSM-enabled configurations.
ConnectionError, ServiceCodeError, LocalityError, ZipCodeError, BuError, InputError, CapacityError, ServiceProviderError: Custom error classes used to handle specific error scenarios.
ErrorCauses, ErrorCodes, ErrorMessages: Objects containing predefined error causes, codes, and messages.
📂 Repository Context:
This function is part of the larger system that interacts with the Centiro API. It is likely used in various parts of the application where data needs to be fetched from the Centiro API. The function also interacts with the logging system and the error handling system of the application.

🔍 Example Usage:
// Example usage
const path = 'GetServiceCompatibility';
const body = { serviceId: '123' };
const requestId = 'abc123';
const version = '1';
const retailId = 'xyz';
const zipCode = '12345';

centiroFetch(path, body, requestId, version, retailId, zipCode)
  .then(response => {
    console.log(response);  // Expected output: JSON response from Centiro service
  })
  .catch(error => {
    console.error(error);  // Handle error
  });
"""

gpt4o_translation = """
### **Function Name: `centiroFetch`**
**📌 Description:**  
This function is responsible for making a fetch request to the Centiro API. It builds the URL for the request, sets the headers, and sends the request with the provided body. If the fetch request fails, it logs the error and throws a `ConnectionError`.

**📥 Parameters:**  
- `path` (*`string`*): The endpoint path for the Centiro API request.
- `body` (*`object`*): The body of the request, which will be stringified and sent as JSON.
- `requestId` (*`string`*): The unique identifier for the request.
- `version` (*`string`*): The version of the Centiro API to use.
- `retailId` (*`string`*): The identifier for the retail location.
- `zipCode` (*`string`*): The zip code for the request.

**📤 Returns:**  
- (*`Promise`*): Returns a Promise that resolves with the response from the Centiro API. If the fetch request fails, it throws a `ConnectionError`.

**🔗 External Dependencies:**  
This function depends on the `Config` module for configuration settings, the `soFetcherObject` for making the fetch request, and various error classes from the `errors` module.

**📂 Repository Context:**  
This function is part of a larger system that interacts with the Centiro API. It is likely used in the context of fetching data related to capacity, service compatibility, and other logistics-related information.

**🔍 Example Usage:**  
```python
# Example usage
try {
  const path = 'GetServiceCompatibility';
  const body = { serviceId: '123' };
  const requestId = 'abc123';
  const version = 'v2';
  const retailId = 'retail1';
  const zipCode = '90210';
  const response = await centiroFetch(path, body, requestId, version, retailId, zipCode);
  console.log(response);  // Expected output: response from Centiro API
} catch (error) {
  console.error(error);  // Expected output: ConnectionError
}
"""