<?php
// Database connection
$host = 'localhost';
$db = 'curly';
$user = 'root'; // default for XAMPP
$pass = 'root'; // XAMPP usually has no password

$conn = new mysqli($host, $user, $pass, $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get form data
$fname = $_POST['fname'];
$lname = $_POST['lname'];
$email = $_POST['email'];
$phone = $_POST['phone'];
$location = $_POST['location'];
$details = $_POST['details'];
$dimension = $_POST['dimension'];
$art_type = $_POST['art_type'];

// Handle file upload
$uploadDir = "uploads/";
$wallImage = $_FILES['wall_image']['name'];
$targetFile = $uploadDir . basename($wallImage);
$imageUploaded = move_uploaded_file($_FILES["wall_image"]["tmp_name"], $targetFile);

// Check if image uploaded successfully
if (!$imageUploaded) {
    die("Image upload failed.");
}

// Insert data into the database (include new fields)
$sql = "INSERT INTO orders (first_name, last_name, email, phone, location, details, dimension, art_type, wall_image) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("sssssssss", $fname, $lname, $email, $phone, $location, $details, $dimension, $art_type, $wallImage);

// Execute
if ($stmt->execute()) {
    echo "Order submitted successfully!";
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
