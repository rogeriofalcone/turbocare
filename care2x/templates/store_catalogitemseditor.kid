<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Catalog Items Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/stores_CatalogItemsEditor.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
  </head>

<body>
	<DIV style="position:relative; width:100%; left:0px; font-size:12px" class="divtable">
		<div class="row">
			<div style="vertical-align:top; width:200px">
				Directories:
				<li py:for="parentitem in parentitems"><a href="CatalogItemsEditor?CatalogItemID=${parentitem['id']}">${parentitem['name']}</a></li>
				<br/>Child items:
				<li py:for="childitem in childitems"><a href="CatalogItemsEditor?CatalogItemID=${childitem['id']}">${childitem['name']}</a></li>
				<br/>Quick Search:
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
			</div>
			<div>
				<form name='CatalogItemForm' action="CatalogItemsEditorSave" method="post">
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="font-size:18px" class="row-blank">${DisplayName}</div>
						<div class="row">
							<div style="width:200px" class="label">Name</div>
							<div><INPUT id="Name" name="Name" type="text" value="${Name}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Description</div>
							<div><TEXTAREA name="Description" rows="4" cols="40">${Description}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Account (for accounting)</div>			
							<div ><INPUT name="Accounting" type="text" value="${Accounting}" size="40"></INPUT></div>
						</div>
					</div>
					<div id="stores2" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px; padding-left:0px" >
								<div style="width:200px" class="label">Fixed Asset</div>
								<div ><INPUT name="IsFixedAsset" type="checkbox" checked="${IsFixedAsset}"></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Service</div>
								<div ><INPUT name="IsService" type="checkbox" checked="${IsService}" ></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">For sale</div>
								<div ><INPUT name="IsForSale" type="checkbox" checked="${IsForSale}"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="stores3" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px; padding-left:0px" >
								<div style="width:150px" class="label">Selectable (actual item)</div>
								<div ><INPUT name="IsSelectable" type="checkbox" checked="${IsSelectable}"></INPUT></div>
							</div>
							<div style="width:400px" >
								<div style="width:300px" class="label">Diespensable (item needs to be dispensed)</div>
								<div ><INPUT name="IsDispensable" type="checkbox" checked="${IsDispensable}"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="registration3" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Min. Stock Amount</div>
							<div ><INPUT name="MinStockAmt" type="text" value="${MinStockAmt}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Reorder Amount</div>
							<div><INPUT name="ReorderAmt" type="text" value="${ReorderAmt}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Tax/VAT</div>
							<div><INPUT name="Tax" type="text" value="${Tax}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnEditCatalogGroups" type="button" value="Catalog Groups" ></input></div>
							<div id="CatalogGroups">
								<li py:for="cataloggroup in cataloggroups">${cataloggroup['name']}</li>
								<INPUT py:for="cataloggroup in cataloggroups" name="CatalogGroups" type="hidden" value="${cataloggroup['id']}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnPickParentItemID" type="button" value="Parent Item" ></input></div>
							<div id="ParentItemID">
								${ParentItemName}
								<INPUT name="ParentItemID" type="hidden" value="${ParentItemID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnPickCompoundID" type="button" value="Compound" ></input></div>
							<div id="CompoundID">
								${CompoundName}
								<INPUT name="CompoundID" type="hidden" value="${CompoundID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnPickPackagingID" type="button" value="Packaging" ></input></div>
							<div id="PackagingID">
								${PackagingName}
								<INPUT name="PackagingID" type="hidden" value="${PackagingID}"></INPUT>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input id="CatalogItemID" type="hidden" name="CatalogItemID" value="${CatalogItemID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="submit" value="Cancel" ></input>
						<input name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input name="Operation" id="btnAddChild" type="submit" value="New sub item" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
					</div>
					<div py:if="not CatalogItemID in ['',None]" id="Items"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="display:table-row">
							<div style="display:table-cell;text-align:center;width:150px">Name</div>
							<div style="display:table-cell;text-align:center">Qty Purchased</div>
							<div style="display:table-cell;text-align:center">Qty Available</div>
							<div style="display:table-cell;text-align:center">Qty Sold</div>
							<div style="display:table-cell;text-align:center">Expire Date</div>
							<div style="display:table-cell;text-align:center">Status</div>
						</div>
						<div py:for="item in stockitems" style="display:table-row">
							<div style="display:table-cell;border-top:1px solid gray">
								<A py:if="not item['ItemID'] in ['',None]" href="StockItemsEditor?StockItemID=${item['ItemID']}">${item['ItemName']}</A>
								<SPAN py:if="item['ItemID'] in ['',None]">${item['ItemName']}</SPAN>
							</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:right">${item['ItemQtyPurchased']}</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:right">${item['ItemQtyAvailable']}</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:right;padding-right:4px">${item['ItemQtySold']}</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:right">${item['ItemExpireDate']}</div>
							<div style="display:table-cell;border-top:1px solid gray">${item['ItemStatus']}</div>
						</div>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
