import unittest
import KazangVoucherProcessor

class TestCases(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()