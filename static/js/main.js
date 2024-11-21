function cancelAppointment(appointmentId) {
    // You can use a modal here for confirmation before proceeding
    if (confirm("Are you sure you want to cancel this appointment?")) {
        // AJAX request to cancel the appointment
        $.ajax({
            url: `/appointments/${appointmentId}/cancel/`,  // Replace with your actual URL
            type: 'POST', 
            data: {
                // Add any CSRF token or data required by your backend
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                // Handle success (e.g., update UI, show message)
                alert("Appointment canceled successfully!");
                location.reload(); // Refresh the page
            },
            error: function(error) {
                // Handle error (e.g., show error message)
                alert("An error occurred. Please try again later.");
                console.error(error);
            }
        });
    }
}


function viewMedicalRecord(recordId) {
    // AJAX request to fetch medical record details
    $.ajax({
        url: `/medical-records/${recordId}/`, // Replace with your actual URL
        type: 'GET',
        success: function(response) {
            // Update modal content and display the modal
            $("#modalTitle").text(`Medical Record - ${response.date_created}`); // Set title
            $("#modalContent").html(`
                <p><strong>Doctor:</strong> ${response.doctor_name}</p>
                <p><strong>Date:</strong> ${response.date_created}</p>
                <p><strong>Diagnosis:</strong> ${response.diagnosis}</p>
                <p><strong>Prescription:</strong> ${response.prescription}</p>
                <p><strong>Notes:</strong> ${response.notes}</p>
            `); 
            $("#medicalRecordModal").removeClass("hidden");
        },
        error: function(error) {
            alert("An error occurred while fetching medical record details.");
            console.error(error);
        }
    });
}

function closeModal() {
    $("#medicalRecordModal").addClass("hidden");
}