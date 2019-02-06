<?php
// Access and authenticate the cloud SQL Database
include "config.php";

//Add unique ID via SQL
//dbContributions
//Add 6-8 digit unique IDs to db Contributions Table
//ALTER TABLE dbContributions ADD `uniquekey` int(10);
//UPDATE dbContributions SET `uniquekey`=ROUND(1+RAND()*99999999) WHERE 1

//Add unique ID via SQL
//dbProducts
//Add 6-8 digit unique IDs to db Products Table
//ALTER TABLE dbProducts ADD `uniquekey` int(10);
//UPDATE dbProducts SET `uniquekey`=ROUND(1+RAND()*99999999) WHERE 1

//Add unique ID via SQL
//dbProvidors
//Add 6-8 digit unique IDs to db Products Table
//ALTER TABLE dbProvidors ADD `uniquekey` int(10);
//UPDATE dbProvidors SET `uniquekey`=ROUND(1+RAND()*99999999) WHERE 1

//Add unique ID via SQL
//dbShipments
//Add 6-8 digit unique IDs to db Products Table
//ALTER TABLE dbShipments ADD `uniquekey` int(10);
//UPDATE dbShipments SET `uniquekey`=ROUND(1+RAND()*99999999) WHERE 1
?>
<?php

    $Search = mysqli_query($con,"SELECT * FROM dbContributions");
            while($Found = mysqli_fetch_array($Search))
            { 
                // If the data has years from 1900s then this code needs to be changed before running
                //09-03-29:17:28 Original Date Time String
                $unique_entry = $Found['uniquekey'];
                $receive_date = $Found['receive_date'];
                $receive_date = "20".substr($receive_date, 0,8);
                $date = new DateTime($receive_date);
                $new_date = $date->format('m/d/Y');
                $result = mysqli_query($con,"UPDATE dbContributions SET receive_date='$new_date' WHERE uniquekey='$unique_entry'"); 
            }    
            
    $Search = mysqli_query($con,"SELECT * FROM dbProducts");
            while($Found = mysqli_fetch_array($Search))
            { 
                $initial_date = "";
                // If the data has years from 1900s then this code needs to be changed before running
                //06-04-25 Original Date Time String
                $unique_entry = $Found['uniquekey'];
                $initial_date = $Found['initial_date'];
                if($initial_date) {
                    $initial_date = "20".substr($initial_date, 0,8);
                    $date = new DateTime($initial_date);
                    $new_date = $date->format('m/d/Y');
                    $result = mysqli_query($con,"UPDATE dbProducts SET initial_date='$new_date' WHERE uniquekey='$unique_entry'"); 
                }
            }                

    $Search = mysqli_query($con,"SELECT * FROM dbShipments");
            while($Found = mysqli_fetch_array($Search))
            { 
                // If the data has years from 1900s then this code needs to be changed before running
                //09-03-29:17:28 Original Date Time String
                //00-09-01:00:63
                $unique_entry = $Found['uniquekey'];
                $receive_date = $Found['receive_date'];
                $receive_date = "20".substr($receive_date, 0,8);
                $date = new DateTime($receive_date);
                $new_date = $date->format('m/d/Y');
                $result = mysqli_query($con,"UPDATE dbContributions SET receive_date='$new_date' WHERE uniquekey='$unique_entry'"); 

            }   

?>
