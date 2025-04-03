import pandas as pd 
import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    """
    Parse the XML file and return a DataFrame.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root

parse_xml('./Data/Apple_Watch/export.xml')
    
def extract_data(root):
    """
    Extract data from the XML tree and return a DataFrame.
    """
    data = []
    for record in root.findall('record'):
        row = {}
        for field in record:
            row[field.tag] = field.text
        data.append(row)
    return data

def to_dataframe(data):
    """
    Convert the extracted data to a DataFrame.
    """
    df = pd.DataFrame(data)
    return df
def save_to_csv(df, filename):
    """
    Save the DataFrame to a CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    
    
def main(xml_file,csv_file):
    """
    Main function to parse XML, extract data, convert to DataFrame, and save to CSV.
    """
    root = parse_xml(xml_file)
    data = extract_data(root)
    df = to_dataframe(data)
    save_to_csv(df, csv_file)
    
if __name__ == "__main__":
    xml_file = './Data/Apple_Watch/export.xml'
    csv_file = './Data/Apple_Watch/export.csv'
    main(xml_file, csv_file)
    
    
    
    
df = pd.read_csv('./Data/Apple_Watch/export.csv')
def read_csv(filename):
    """
    Read the CSV file and return a DataFrame.
    """
    df = pd.read_csv(filename)
    return df


df = pd.read_xml('./Data/Apple_Watch/export.xml')
df.head(20)