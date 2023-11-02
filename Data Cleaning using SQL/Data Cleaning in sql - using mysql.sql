/*

Cleaning Data in SQL Queries

*/

use project ;

-- Changing Data Type and Standarize Date 

select saledate from nashvillehousing;

update nashvillehousing 
set saledate = replace(saledate,',','');

update nashvillehousing 
set saledate = str_to_date(saledate,'%M %d %Y');

alter table nashvillehousing modify saledate date;


----------------------------------------------------------------------------------------------------------------------------------------------------------

-- Populate Property Address data 

select * from nashvillehousing
where propertyaddress = '';



Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress,if(a.propertyaddress='',b.propertyaddress,a.propertyaddress)
From nashvillehousing a
JOIN nashvillehousing b
	on a.ParcelID = b.ParcelID
	AND a.UniqueID <> b.UniqueID
Where a.PropertyAddress = '';


update  nashvillehousing a
JOIN nashvillehousing b
	on a.ParcelID = b.ParcelID
	AND a.UniqueID <> b.UniqueID
set a.propertyaddress = if(a.propertyaddress='',b.propertyaddress,a.propertyaddress)
Where a.PropertyAddress = '';


----------------------------------------------------------------------------------------------------------------------------------------------------------

-- Breaking out Address into Individual Columns (Address, City, State)

select substring(PropertyAddress,1,locate(',',Propertyaddress)-1),
substring(PropertyAddress,locate(',',Propertyaddress)+1,length(PropertyAddress))
 from nashvillehousing ;


alter table nashvillehousing add PropertySplitAddress Nvarchar(255);

update nashvillehousing 
set PropertySplitAddress = substring(PropertyAddress,1,locate(',',Propertyaddress)-1);


alter table nashvillehousing add PropertySplitCity Nvarchar(255);

update nashvillehousing 
set PropertySplitCity = substring(PropertyAddress,locate(',',Propertyaddress)+1,length(PropertyAddress));

select * from nashvillehousing ;


select OwnerAddress 
from nashvillehousing;


Select
substring_index(OwnerAddress,',',1),
substring_index(OwnerAddress,',',2),
substring_index(OwnerAddress,',',-1)
from nashvillehousing ;



alter table nashvillehousing
add OwnerSplitAddress Nvarchar(255);

update nashvillehousing
set OwnerSplitAddress = substring_index(OwnerAddress,',',1);


alter table nashvillehousing
add OwnerSplitCity Nvarchar(255);

update nashvilleHousing
set OwnerSplitCity = substring_index(OwnerAddress,',',2);


alter table nashvillehousing
add OwnerSplitState Nvarchar(255);

update nashvillehousing
SET OwnerSplitState = substring_index(OwnerAddress,',',-1);



Select *
from nashvillehousing;


----------------------------------------------------------------------------------------------------------------------------------------------------------

-- Change Y and N to Yes and No in "Sold as Vacant" field

select distinct SoldAsVacant 
from nashvillehousing;

select SoldAsVacant,
case when SoldAsVacant = "N" then "No" 
     when SoldAsVacant = "Y" then "Yes"
    else SoldAsVacant
    end
from nashvillehousing;

update nashvillehousing 
set SoldAsVacant = case when SoldAsVacant = "N" then "No" 
     when SoldAsVacant = "Y" then "Yes"
    else SoldAsVacant
    end;
    

----------------------------------------------------------------------------------------------------------------------------------------------------------

-- Remove Duplicates

with rownumcte AS(
Select *,
	ROW_NUMBER() OVER (
	PARTITION BY ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY
					UniqueID
					) row_num
from nashvillehousing 
)
Select *
From RowNumCTE
Where row_num > 1
Order by PropertyAddress;



with rownumcte as(
Select *,
	ROW_NUMBER() OVER (
	PARTITION BY ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY
					UniqueID
					) row_num
from nashvillehousing 
)
delete from nashvillehousing using nashvillehousing join rownumcte on nashvillehousing.uniqueid = rownumcte.uniqueid 
where rownumcte.row_num >1 ;

select count(*) from nashvillehousing;
--------------------------------------------------------------------------------------------------------------------------------------------------------

-- Delete Unused Columns

alter table nashvillehousing 
drop OwnerAddress, 
drop TaxDistrict,
drop  PropertyAddress, 
drop SaleDate;



