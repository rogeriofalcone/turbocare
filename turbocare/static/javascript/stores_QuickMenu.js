function postJSON_QuickMenu(url, postVars) {
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}

connect(window, 'onload', function(){
	var Menu = getElement("LeftMenu");
	var Title = getElement('LeftMenuTitle');
	if (Menu!=null&&Title!=null){
		var d = postJSON_QuickMenu('PopUpMenu');
		d.addCallbacks(RenderPopUpMenu);
	}
});
var RenderPopUpMenu = function(d) {
	var Menu = getElement("LeftMenu");
	var Title = getElement('LeftMenuTitle');
	appendChildNodes(Title,d.LocationName+' Menu');
	if (d.CatalogItemsEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'CatalogItemsEditor'},'Item master')));
	}
	if (d.PurchaseOrdersEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'PurchaseOrdersEditor'},'Purchase orders')));
	}
	if (d.GoodsReceivedEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'GoodsReceivedEditor'},'Goods received')));
	}
	if (d.QuoteRequestsEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'QuoteRequestsEditor'},'Quote Requests')));
	}
	if (d.QuotesEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'QuotesEditor'},'Quotes')));
	}
	if (d.StockMonitor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'StockMonitor'},'Stock monitor')));
	}
	if (d.StockItemsEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'StockItemsEditor'},'Stock editor')));
	}
	if (d.StockTransferRequestsEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'StockTransferRequestsEditor'},'Stock transfer requests')));
	}
	if (d.StockTransfersEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'StockTransfersEditor'},'Stock transfers')));
	}
	if (d.VendorsEditor==true) {
		Menu.appendChild(DIV({'style':'display:none'},A({'href':'VendorsEditor'},'Vendors')));
	}
}
