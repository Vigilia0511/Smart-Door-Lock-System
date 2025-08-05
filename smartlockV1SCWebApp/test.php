<?php
$responseMessage = "";

// Map actions to their respective endpoints and payloads
$actionMapping = [
    'open_solenoid_lock_on' => ['url' => "http://192.168.216.237:5000/control_solenoid", 'payload' => 'switch=on'],
    'open_solenoid_lock_off' => ['url' => "http://192.168.216.237:5000/control_solenoid", 'payload' => 'switch=off'],
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $inputData = json_decode(file_get_contents('php://input'), true);
    $switchAction = $inputData['action'] ?? '';

    if (array_key_exists($switchAction, $actionMapping)) {
        $actionDetails = $actionMapping[$switchAction];
        $url = $actionDetails['url'];
        $postData = $actionDetails['payload'];

        $curl = curl_init($url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $postData);

        $response = curl_exec($curl);

        if (curl_errno($curl)) {
            echo json_encode(["status" => "error", "message" => curl_error($curl)]);
        } else {
            echo json_encode(["status" => "success"]);
        }

        curl_close($curl);
    } else {
        echo json_encode(["status" => "error", "message" => "Invalid action received."]);
    }
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solenoid Lock Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            text-align: center;
        }
        header {
            background-color: #556B2F;
            color: white;
            padding: 10px 0;
        }
        button {
            color: white;
            background-color: black;
            border: none;
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            opacity: 0.8;
        }
        .control-container {
            margin: 20px auto;
            background: #333;
            color: white;
            padding: 15px;
            border-radius: 10px;
            display: inline-block;
        }
        .control-row {
            margin: 15px 0;
            display: flex;
            justify-content: space-between;
        }
        .on-button {
            background-color: white;
            color: black;
        }
        .off-button {
            background-color: red;
        }
    </style>
</head>
<body>
    <div class="control-container">
        <div class="control-row">
            <label>OPEN DOOR LOCK</label>
            <button id="doorLockOn" class="on-button" onclick="sendRequest('open_solenoid_lock_on')">OPEN</button>
            <button id="doorLockOff" class="off-button" onclick="sendRequest('open_solenoid_lock_off')">CLOSE</button>
        </div>
    </div>

    <script>
        function sendRequest(action) {
            const notificationArea = document.getElementById('notification-area');

            fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action })
            })
            .then(response => response.json())
            .then(data => {
            
            })
            .catch(error => {
                notificationArea.textContent = `Error: ${error.message}`;
            });
        }
    </script>
</body>
</html>
