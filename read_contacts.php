<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "phonebook";

// ایجاد اتصال
$conn = new mysqli($servername, $username, $password, $dbname);

// بررسی اتصال
if ($conn->connect_error) {
    die("اتصال برقرار نشد: " . $conn->connect_error);
}

$sql = "SELECT name, phone, email FROM contacts";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["name"]. "</td><td>" . $row["phone"]. "</td><td>" . $row["email"]. "</td></tr>";
    }
} else {
    echo "<tr><td colspan='3'>نتیجه‌ای یافت نشد</td></tr>";
}
$conn->close();
?>
