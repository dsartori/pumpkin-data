SELECT Reference_Date,Converted_UOM,SUM(Converted_Quantity) 
FROM Production 
WHERE Measure='Total production'
AND Geography='Canada' 
GROUP BY Reference_Date;