code_snippet = """
export async function getAssemblyServicePrice(
  itemNo: string,
  retailId: string,
  context: Context,
  quantity: number,
): Promise<Nullable<AssemblyServicePrice>> {
  const res = await context.Loader.load(salesItemSalesPricesLoaderFunc, { itemNo, retailId, context });

  if (!res?.servicePrices || !res?.servicePrices?.length) {
    return null;
  }

  const servicePrices = res.servicePrices?.find(
    (servicePrice) => Config.config.services.assembly.type === servicePrice.serviceProductId,
  );

  if (!servicePrices) {
    return null;
  }

  const transformedPrice = transformPrices(
    servicePrices.priceInclTax,
    servicePrices.priceExclTax,
    servicePrices.indicativeTotalTax,
  );
  if (transformedPrice === undefined) {
    return null;
  }

  return {
    total: {
      inclTax: twoDecimalDigits(transformedPrice.inclTax * quantity),
      exclTax: twoDecimalDigits(transformedPrice.exclTax * quantity),
      tax: twoDecimalDigits(transformedPrice.tax * quantity),
    },
    each: {
      inclTax: twoDecimalDigits(transformedPrice.inclTax),
      exclTax: twoDecimalDigits(transformedPrice.exclTax),
      tax: twoDecimalDigits(transformedPrice.tax),
    },
  };
}
"""



prompt1_translation = """
### **Function Name: `getAssemblyServicePrice`**
**📌 Description:**  
This function fetches the assembly service price for a specific item from the Erix service. It returns the total and individual prices, both including and excluding tax.

**📥 Parameters:**  
- `itemNo` (*String*): The item number.
- `retailId` (*String*): The retail ID.
- `context` (*Object*): The context object, which includes the Loader for data fetching.
- `quantity` (*Number*): The quantity of the item.

**📤 Returns:**  
- (*Object*): An object containing the total and individual prices, both including and excluding tax. If no service prices are found, it returns null.

**🔍 Example Usage:**  
```python
# Example usage
result = getAssemblyServicePrice('123', 'abc', context, 2)
print(result)  # Expected output: Object with total and individual prices
```
"""

prompt2_translation = """
The `getAssemblyServicePrice` function is an asynchronous function that takes an item number, retail ID, context, and quantity as arguments. It loads sales prices data using the `salesItemSalesPricesLoaderFunc` function. If there are no service prices, it returns null. Otherwise, it finds the service prices that match the assembly type specified in the configuration. It then transforms the prices using the `transformPrices` function and returns the total and each price, both including and excluding tax, rounded to two decimal places.
"""