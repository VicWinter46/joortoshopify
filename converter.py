import pandas as pd

def convert_joor_to_shopify(input_excel_path, sheet_name="PO# 17680092"):
    """
    Reads the JOOR 'to size' Excel file and converts it into a Shopify-ready CSV.
    """
    # Read the Excel file. Adjust header row if necessary (here assumed to be row 17, index=16).
    df = pd.read_excel(input_excel_path, sheet_name=sheet_name, header=16)
    
    # Define the size columns.
    size_columns = ['XS', 'S', 'M', 'L', 'XL']
    
    shopify_rows = []

    for idx, row in df.iterrows():
        # Retrieve basic product details and strip any extra spaces.
        style_number = str(row.get('Style Number', '')).strip()
        style_name = str(row.get('Style Name', '')).strip()
        color = str(row.get('Color', '')).strip()
        
        # Create a unique handle using the style number.
        handle = style_number
        # Create a title combining style name and color.
        title = f"{style_name} - {color}"
        # Get image URL if available.
        image_url = row.get('Style Image', '')
        
        # Get pricing information: suggested retail and wholesale (cost).
        sugg_retail = row.get('Sugg. Retail (USD)', None)
        wholesale = row.get('WholeSale (USD)', None)  # This is your cost.
        
        # Loop over each size column.
        for size in size_columns:
            quantity = row.get(size, 0)
            # If quantity is missing, treat it as zero.
            if pd.isna(quantity):
                quantity = 0
            # Only create a variant if quantity is greater than zero.
            if quantity > 0:
                # Create a unique SKU by combining style number and size.
                variant_sku = f"{style_number}-{size}"
                shopify_rows.append({
                    "Handle": handle,
                    "Title": title,
                    "Option1 Name": "Size",
                    "Option1 Value": size,
                    "Variant SKU": variant_sku,
                    "Variant Inventory Qty": quantity,
                    "Variant Price": sugg_retail,
                    "Variant Cost": wholesale,
                    "Image URL": image_url,
                    "Vendor": "Marie Oliver"
                })
    
    shopify_df = pd.DataFrame(shopify_rows)
    return shopify_df

if __name__ == "__main__":
    # Example usage: update the input file path to your local test file if needed.
    input_excel_path = "path/to/your/JOOR_file.xlsx"  # Replace with your file path.
    output_csv_path = "joor_to_shopify.csv"
    df = convert_joor_to_shopify(input_excel_path)
    df.to_csv(output_csv_path, index=False)
    print("Shopify CSV conversion completed. File saved at:", output_csv_path)
