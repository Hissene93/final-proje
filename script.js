
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

  
    const modalForms = document.querySelectorAll('.modal-form')
    modalForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault()
            
            this.submit()
        })
    })


    const deleteButtons = document.querySelectorAll('.btn-delete')
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                e.preventDefault()
            }
        })
    })
})


function toggleStudentFields() {
    const roleSelect = document.getElementById('role')
    const studentFields = document.getElementById('studentFields')
    
    if (roleSelect.value === 'student') {
        studentFields.style.display = 'block'
    } else {
        studentFields.style.display = 'none'
    }
}


document.addEventListener('DOMContentLoaded', toggleStudentFields)