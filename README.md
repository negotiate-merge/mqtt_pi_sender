This is just a basic little program that I have set up on a respberry Pi at home. It is a simulator for real world cellular connected data loggers.

Mock data is aggregated and sent at two hour intervals. The data is constructed in the same format as what would be expected to be received from this device
https://www.dragino.com/products/nb-iot/item/290-ps-nb-na.html which is the intended use case.

Data is sent securely using mqtt with TLS as if the devices were really deployed in the wild. The only component that is not implemented is transport 
over a cellular network.
