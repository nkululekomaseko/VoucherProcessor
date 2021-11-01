#voucherFileName = input("Enter file name for processing:\n")

# Global Variables
voucherFileName = "KazangBulkVouchers_Demo.txt" 
voucherFileObj = None
headerDictionary = {}
voucherDataList = []

# VoucherData class stores data dictionary {property: value} and ordered line item list
class VoucherData:

    # Class variable -> Store cumulative count and value per voucher type 
    voucherSummaryDictionary = {}

    """
        voucherFields is a list of fields obtained from the file
        lineItems is a list containing line items as they appear in the file
        fileDataCSV is the unprocessed CSV-formatted line containng the data as describled by voucherFields
    """
    def __init__(self, voucherFields, lineItems, fileDataCSV):
        self.voucherDataDictionary = {}
        self.lineItemData = []

        fileDataArray = fileDataCSV.split(",")

        for fieldIndex in range(len(voucherFields)):
            self.voucherDataDictionary[voucherFields[fieldIndex]] = fileDataArray[fieldIndex]

        for item in lineItems:
            if (item == "empty"):
                self.lineItemData.append(item)
            else:
                self.lineItemData.append(self.voucherDataDictionary[item])

        #Obtain voucher value from description
        voucherDescription = self.voucherDataDictionary["description"]
        voucherValue = float(voucherDescription.split(" ")[1])

        # Update total vouchers and total value per voucher type. e.g. total Cell-C voucher count and value
        if (voucherDescription not in VoucherData.voucherSummaryDictionary):
            VoucherData.voucherSummaryDictionary[voucherDescription] = [voucherValue, 1, voucherValue]
        else:
            updatedCount = VoucherData.voucherSummaryDictionary[voucherDescription][1] + 1  
            VoucherData.voucherSummaryDictionary[voucherDescription] = [voucherValue, updatedCount, voucherValue * updatedCount]

    def printVoucherData(self):
        for voucherKey in self.voucherDataDictionary:
            print(voucherKey, ": ", self.voucherDataDictionary[voucherKey], sep="")

    def printLineItemData(self):
        for item in self.lineItemData:
            print(item)

# File processing
def processVoucherFile():
    try:
        voucherFileObj = open(voucherFileName, "r")
        nextLine = voucherFileObj.readline()

        # Line processing and adding header parameters in the header dictionary, terminates at voucher_fields
        while nextLine:
            nextLine = nextLine.rstrip("\n")

            if (nextLine.startswith("line_item")):
                if ("line_item" not in headerDictionary):
                    headerDictionary["line_item"] = [nextLine[nextLine.index(':') + 1:]]
                else:
                    headerDictionary["line_item"].append(nextLine[nextLine.index(':') + 1:])
            
            elif (nextLine.startswith("voucher_summary")):
                if ("voucher_summary" not in headerDictionary):
                    headerDictionary["voucher_summary"] = [nextLine[nextLine.index(':') + 1:].split(",")]
                else:
                    headerDictionary["voucher_summary"].append(nextLine[nextLine.index(':') + 1:].split(","))

            elif (nextLine.startswith("voucher_fields")):
                headerDictionary["voucher_fields"] = nextLine[nextLine.index(':') + 1:].split(",")
                nextLine = voucherFileObj.readline()
                break

            else:
                headerDictionary[nextLine[:nextLine.index(':')]] = nextLine[nextLine.index(':') + 1:]
            
            nextLine = voucherFileObj.readline()

        #print(headerDictionary)

        # Line processing, creating VoucherData objects and adding them in a list (voucherDataList)
        while nextLine:
            nextLine = nextLine.rstrip("\n")

            voucherDataList.append(VoucherData(
                    headerDictionary["voucher_fields"],
                    headerDictionary["line_item"],
                    nextLine 
                )
            )
            nextLine = voucherFileObj.readline()

        voucherFileObj.close()

    except IOError:
        print ("Error: File \"%s\" does not exist." % voucherFileName)
        exit()
    
# Voucher validation, compare expected voucher summary with calculated values from voucherData body
def validateVoucherSummary(headerVoucherSummary):
    terminateProgram = False

    print(VoucherData.voucherSummaryDictionary)
    print(headerVoucherSummary)

    # Iterate through all the voucher summary entries from the header data and compare calculated vs expected values.
    for voucherSummaryItem in headerVoucherSummary:
        voucherDescription = voucherSummaryItem[0]

        # Voucher summary data from header
        voucherExpectedCount = int(voucherSummaryItem[1])
        voucherExpectedValue = float(voucherSummaryItem[2])

        # Calculated summary data from VoucerData class
        voucherCalculatedCount = VoucherData.voucherSummaryDictionary[voucherDescription][1]
        voucherCalculatedValue = VoucherData.voucherSummaryDictionary[voucherDescription][2]

        # Produce appropriate error when calculated values don't correspond with expected values
        if (voucherExpectedCount != voucherCalculatedCount):
            print("Error: Expected a total count of %d for %s vouchers, received %d" % (voucherExpectedCount, voucherDescription, voucherCalculatedCount))
            terminateProgram = True
        elif (voucherExpectedValue != voucherCalculatedValue):
            print("Error: Expected a cumulative value of R%.2f for %s vouchers, received R%.2f" % (voucherExpectedValue, voucherDescription, voucherCalculatedValue))
            terminateProgram = True

    if (terminateProgram):
        exit()

    # If validation passes, return true
    return True
         
#Write processed data to a file
def writeDataToFile():
    finalOutput = ""
    count = 0
    lineCounter = 0
    voucherSize = len(voucherDataList)

    # Iterate through all voucher data objects, use lineItems to reference expected structure
    while count < voucherSize:

        #For every line item (pin, empty, ...)
        for lineIndex in range(len(headerDictionary["line_item"])):
            columnCount = int(headerDictionary["columns"])
            leftMargin = int(headerDictionary["left_margin"])

            # For every column count
            for column in range(columnCount):
                count = count + 1 if lineIndex == 0 else count
                voucherDataIndex = lineCounter * columnCount + column
                if (voucherDataIndex >= voucherSize):
                    break
                cellData = voucherDataList[voucherDataIndex].lineItemData[lineIndex]

                if (cellData == "empty"):
                    break
                else:
                    columnWidthSpacing = int(headerDictionary["column_width"]) + int(headerDictionary["column_spacing"])
                    finalOutput = finalOutput + "{:<{space}}".format("", space = leftMargin) if column == 0 else finalOutput    # Add left margin
                    finalOutput += "{:<{space}}".format(cellData, space = columnWidthSpacing)                                   # Add appropriate column spacing
                if (count > voucherSize):
                    continue
            finalOutput += "\n"

        rowSpacing = int(headerDictionary["row_spacing"])  
        finalOutput += "\n" * rowSpacing

        lineCounter += 1

    # Assumption: All processed files have a .txt extension.
    # Write the final result into a file, append "_result" from the original filename
    voucherResultFileName = voucherFileName[:voucherFileName.index(".txt")] + "_result" + ".txt"
    newFile = open(voucherResultFileName, "w")
    newFile.write(finalOutput)
    newFile.close()

# Main method
if __name__ == "__main__":
    processVoucherFile()
    validateVoucherSummary(headerDictionary["voucher_summary"])
    writeDataToFile()










