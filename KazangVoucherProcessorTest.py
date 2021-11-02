import unittest
import KazangVoucherProcessor

class TestCases(unittest.TestCase):

    # Test header data processing from file (Datetime)
    def testHeaderDataProcessingDateTime(self):
        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertEqual(KazangVoucherProcessor.headerDictionary['download_datetime'], '2015-11-06 1357')
        self.assertEqual(KazangVoucherProcessor.headerDictionary['order_datetime'], '2015-11-05 1014')

    # Test header data processing from file (Layout name, formatting properties)
    def testHeaderDataProcessingFormatting(self):
        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertEqual(KazangVoucherProcessor.headerDictionary['layout_name'], 'Demo')
        self.assertEqual(KazangVoucherProcessor.headerDictionary['columns'], '5')
        self.assertEqual(KazangVoucherProcessor.headerDictionary['column_width'], '25')
        self.assertEqual(KazangVoucherProcessor.headerDictionary['column_spacing'], '5')
        self.assertEqual(KazangVoucherProcessor.headerDictionary['left_margin'], '0')
        self.assertEqual(KazangVoucherProcessor.headerDictionary['row_spacing'], '5')

    # Test header data processing from file (Line item)
    def testHeaderDataProcessingLineItem(self):
        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertListEqual(KazangVoucherProcessor.headerDictionary['line_item'], ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date'])

    # Test header data processing from file (Voucher Summary)
    def testHeaderDataProcessingVoucherSummary(self):
        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertListEqual(KazangVoucherProcessor.headerDictionary['voucher_summary'], [['Cell-C 10.00', '10', '100.00'], ['MTN 5.00', '5', '25.00'], ['Vodacom 12.00', '5', '60.00']])

    # Test header data processing from file (Voucher Fields)
    def testHeaderDataProcessingVoucherFields(self):
        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertListEqual(KazangVoucherProcessor.headerDictionary['voucher_fields'], ['description', 'pin', 'serial_number', 'expiry_date'])

    # Testing voucher object instance and object dictionary property
    def testVoucherDataDictionary(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date']
        fileDataCSV = "Cell-C 10.00,6374897623,100000000,2020-01-01"

        voucherDataObj = KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV)

        self.assertDictEqual(voucherDataObj.voucherDataDictionary, {
            'description': 'Cell-C 10.00', 
            'pin': '6374897623', 
            'serial_number': '100000000', 
            'expiry_date': '2020-01-01'
        })

    # Testing voucher data class variable -> voucherSummaryDictionary (one entry)
    def testVoucherDataSummaryDictionaryOne(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date']
        fileDataCSV = "Cell-C 10.00,6374897623,100000000,2020-01-01"

        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV)

        self.assertDictEqual(KazangVoucherProcessor.VoucherData.voucherSummaryDictionary, {'Cell-C 10.00': [10.0, 1, 10.0]})

    # Testing voucher data class variable -> voucherSummaryDictionary (three entries)
    def testVoucherDataSummaryDictionaryThree(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date']
        fileDataCSV1 = "Cell-C 10.00,6374897623,100000000,2020-01-01"
        fileDataCSV2 = "Cell-C 10.00,6323457623,100000001,2020-01-01"
        fileDataCSV3 = "Cell-C 5.00,6376896666,100000002,2020-01-01"

        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV1)
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV2)
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV3)

        self.assertDictEqual(KazangVoucherProcessor.VoucherData.voucherSummaryDictionary, {
            'Cell-C 10.00': [10.0, 2, 20.0], 
            'Cell-C 5.00': [5.0, 1, 5.0]
        })

    # Testing voucher data class variable -> voucherSummaryDictionary (File data)
    def testVoucherDataSummaryDictionaryFile(self):

        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertDictEqual(KazangVoucherProcessor.VoucherData.voucherSummaryDictionary, {
            'Cell-C 10.00': [10.0, 10, 100.0], 
            'MTN 5.00': [5.0, 5, 25.0], 
            'Vodacom 12.00': [12.0, 5, 60.0]
        })

    # Testing voucher summary validation (one entry)
    def testVoucherSummaryValidationOne(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date']
        fileDataCSV = "Cell-C 10.00,6374897623,100000000,2020-01-01"

        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV)

        self.assertTrue(KazangVoucherProcessor.validateVoucherSummary([['Cell-C 10.00', '1', '10.00']]))

    # Testing voucher summary validation (three entries)
    def testVoucherSummaryValidationThree(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date']
        fileDataCSV1 = "Cell-C 10.00,6374897623,100000000,2020-01-01"
        fileDataCSV2 = "Cell-C 10.00,6323457623,100000001,2020-01-01"
        fileDataCSV3 = "Cell-C 5.00,6376896666,100000002,2020-01-01"

        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV1)
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV2)
        KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV3)

        self.assertTrue(KazangVoucherProcessor.validateVoucherSummary([['Cell-C 10.00', '2', '20.00'], ['Cell-C 5.00', '1', '5.00']]))

    # Testing voucher summary validation (File data)
    def testVoucherSummaryValidationFile(self):
        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertTrue(KazangVoucherProcessor.validateVoucherSummary([['Cell-C 10.00', '10', '100.00'], ['MTN 5.00', '5', '25.00'], ['Vodacom 12.00', '5', '60.00']]))

    # Testing one line item
    def testVoucherDataLineItem(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin']
        fileDataCSV = "Cell-C 10.00,6374897623,100000000,2020-01-01"

        voucherDataObj = KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV)

        self.assertEqual(voucherDataObj.lineItemData, ['6374897623'])

    # Testing line items and verifying alignment 
    def testVoucherDataLineItems(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date']
        fileDataCSV = "Cell-C 10.00,6374897623,100000000,2020-01-01"

        voucherDataObj = KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV)

        self.assertEqual(voucherDataObj.lineItemData, ['6374897623', 'empty', 'empty', 'Cell-C 10.00', '100000000', '2020-01-01'])

    # Testing line items with additional properties and duplications, verifying alignment 
    def testVoucherDataLineItems2(self):
        voucherFields = ['description', 'pin', 'serial_number', 'expiry_date']
        lineItems = ['pin', 'empty', 'empty', 'description', 'serial_number', 'expiry_date', 'empty', 'empty', 'pin']
        fileDataCSV = "Cell-C 10.00,6374897623,100000000,2020-01-01"

        voucherDataObj = KazangVoucherProcessor.VoucherData(voucherFields, lineItems, fileDataCSV)

        self.assertEqual(voucherDataObj.lineItemData, ['6374897623', 'empty', 'empty', 'Cell-C 10.00', '100000000', '2020-01-01', 'empty', 'empty', '6374897623'])

    # Test result filename
    def testResultFileName(self):
        fileName = "KazangBulkVouchers_Demo.txt"
        KazangVoucherProcessor.clearGlobalVariables()
        KazangVoucherProcessor.processVoucherFile(fileName)

        self.assertEqual(KazangVoucherProcessor.writeDataToFile(), 'KazangBulkVouchers_Demo_result.txt')

if __name__ == '__main__':
    unittest.main()