<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
 
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/registration_search.js" TYPE="text/javascript"></SCRIPT>
    <title>${LocationName} Store</title>
</head>
<body>
 	<DIV class="big_text_1">${LocationName} Store
		<DIV class="big_text_2">Menu</DIV>
			<div style="width:80%; left:10px; position:relative; font-size:14px" class="divtable">
				<div py:if="IsStore" class="row">
					<div py:if="'stores_catalog_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="CatalogItemsEditor">Item master</a></div>
					<div py:if="'stores_catalog_view' in tg.identity.permissions" style="text-align: left" class="clear">
						Edit/Add/Remove items in the Item master table
					</div>
				</div>
				<div py:if="IsStore" class="row">
					<div py:if="'stores_po_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="PurchaseOrdersEditor">Purchase orders</a></div>
					<div py:if="'stores_po_view' in tg.identity.permissions" style="text-align: left" class="clear">
						View/Add/Edit/Remove purchase orders
					</div>
				</div>
				<div py:if="IsStore and CanReceive" class="row">
					<div py:if="'stores_gr_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="GoodsReceivedEditor">Goods received</a></div>
					<div py:if="'stores_gr_view' in tg.identity.permissions" style="text-align: left" class="clear">
						View/Add/Edit/Remove goods received (for ${LocationName})
					</div>
				</div>
				<div py:if="IsStore" class="row">
					<div py:if="'stores_quoterequest_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="QuoteRequestsEditor">Quote Requests</a></div>
					<div py:if="'stores_quoterequest_view' in tg.identity.permissions" style="text-align: left" class="clear">
						Add/Edit/Remove quote requests
					</div>
				</div>
				<div py:if="IsStore" class="row">
					<div py:if="'stores_quote_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="QuotesEditor">Quotes</a></div>
					<div py:if="'stores_quote_view' in tg.identity.permissions" style="text-align: left" class="clear">
						Add/Edit/Remove quotes
					</div>
				</div>
				<div class="row">
					<div style="text-align: left" class="clear"><a href="StockMonitor">Stock monitor</a></div>
					<div style="text-align: left" class="clear">
						View current stock status (for ${LocationName})
					</div>
				</div>
				<div py:if="IsStore" class="row">
					<div py:if="'stores_stock_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="StockItemsEditor">Stock editor</a></div>
					<div py:if="'stores_stock_view' in tg.identity.permissions" style="text-align: left" class="clear">
						Add/Edit/Remove stock
					</div>
				</div>
				<div py:if="IsStore" class="row">
					<div py:if="'stores_stocktransferrequest_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="StockTransferRequestsEditor">Stock transfer requests</a></div>
					<div py:if="'stores_stocktransferrequest_view' in tg.identity.permissions" style="text-align: left" class="clear">
						Add/Edit/Remove stock transfer requests (for ${LocationName})
					</div>
				</div>
				<div class="row">
					<div py:if="'stores_stocktransfer_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="StockTransfersEditor">Stock transfers</a></div>
					<div py:if="'stores_stocktransfer_view' in tg.identity.permissions" style="text-align: left" class="clear">
						Add/Edit/Remove stock transfers (for ${LocationName})
					</div>
				</div>
				<div py:if="IsStore" class="row">
					<div py:if="'stores_vendor_view' in tg.identity.permissions" style="text-align: left" class="clear"><a href="VendorsEditor">Vendors</a></div>
					<div py:if="'stores_vendor_view' in tg.identity.permissions" style="text-align: left" class="clear">
						Add/Edit/Remove Vendors
					</div>
				</div>
			</div>
	</DIV>
</body>
</html>
