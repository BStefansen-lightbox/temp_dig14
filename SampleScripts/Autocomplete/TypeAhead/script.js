$(document).ready(function() {
    var apiKey = ""

    function extractKey() {
        var keyBox = document.getElementById("input-key");
        apiKey = keyBox.value;
    }

    function authorizationTest() {
        $.ajax({
            url: "https://api.lightboxre.com/v1/addresses/_autocomplete",
            method: "GET",
            headers: {
                "x-api-key": apiKey
            },
            data: {
                text: "5209 Cal",
                countryCode: "US"
            },
            success: function(data, textStatus, xhr) {
                alert("Authorization Successful");
            },
            error: function(xhr, status, error) {
                alert("Authorization Failed, Error: " + error);
            }
        });

    }
    
    // Add an event listener to the button
    document.getElementById("apiButton").addEventListener("click", function() {
        // Call the function from the separate JavaScript file
        extractKey();
        authorizationTest();
    });


    $("#input-text").on("input", function() {
        var inputValue = $(this).val();
        if (inputValue.length > 3) {
            fetchDropdown(inputValue);
        } else {
            $("#dropdown").empty(); // Clear dropdown if input field is empty
        }
    });

    function fetchDropdown(inputValue) {
        $.ajax({
            url: "https://api.lightboxre.com/v1/addresses/_autocomplete",
            method: "GET",
            headers: {
                "x-api-key": apiKey
            },
            data: {
                text: inputValue,
                countryCode: "US"
            },
            success: function(data) {
                renderDropdown(data.addresses);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    }
    

    function renderDropdown(addresses) {
        var dropdownOptions = addresses.map(function(item) {
            return $("<option>").text(item.label);
        });
        $("#dropdown").empty().append(dropdownOptions);
        $("#dropdown").prop("size", addresses.length); // Set dropdown size to show all options
        $("#dropdown").prop("multiple", true); // Allow multiple selections
    }
});
