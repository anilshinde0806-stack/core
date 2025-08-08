// Confirm script is loaded
console.log("modal.js loaded!");

// Show the login modal via AJAX
function showLoginModal() {
    $.ajax({
        url: "/ajax/login/",  // Or {% url 'login_modal' %}
        type: "GET",
        success: function (data) {
            $('#loginModalContent').html(data);
            const modal = new bootstrap.Modal(document.getElementById('loginModal'), {
                backdrop: 'static',
                keyboard: false
            });
            modal.show();
        },
        error: function () {
            alert('Failed to load login form.');
        }
    });
}


// ✅ Re-bind form submission after modal loads

    $(document).on('submit', '#loginForm', function (e) {
    e.preventDefault();
    $("#loginButton").prop("disabled", true);
    $("#loginSpinner").removeClass("d-none");

    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function (response) {
            console.log("Login response:", response);  // Debug
            if (response.success) {
                window.location.href = response.redirect_url;
            } else {
                $("#loginError").text(response.error || "Login failed.");
                $("#loginButton").prop("disabled", false);
                $("#loginSpinner").addClass("d-none");
            }
        },
        error: function () {
            $("#loginError").text("Server error occurred.");
            $("#loginButton").prop("disabled", false);
            $("#loginSpinner").addClass("d-none");
        }
    });
});


