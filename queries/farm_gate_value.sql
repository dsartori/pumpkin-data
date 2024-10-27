SELECT Reference_Date,Converted_UOM,SUM(Converted_Quantity) 
FROM Production 
WHERE Measure='Farm gate value' 
AND Geography='Canada' 
GROUP BY Reference_Date;