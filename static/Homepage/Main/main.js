// USE FOR THE SIDEBAR
const emails = document.getElementById('emails');
const application = document.getElementById('application');
const schedule = document.getElementById('schedule');
const grades = document.getElementById('grades');
const about = document.getElementById('about');

//THE COMPONENT TO CHANGE THE INNERHTML
const container = document.getElementById('content');

// DATA MAPS
const cities = {
    zamboanga_del_sur: ['Zamboanga City', 'Ipil', "Basilan"]
};

const barangay_list = {
    zamboanga_city: ['Culianan', 'Mercedes', 'Pasobolong', 'Boalan', "Divisoria"]
};

const courses = {
    ccje: ['Criminology'],
    ce: ['Electrical Engineering', 'Civil Engineering', 'Electronics Engineering']
};

// FOR APPLICATION PROCESSING
application.addEventListener('click', function() {
    fetch('/user_status')
    .then(response => response.json())
    .then(data => {
        if (data.status === "None") {
            container.innerHTML = `
            <h1>You Havent Applied Yet.</h1>
            <h3>Press the button to Apply</h3>
            <button id="start-application">Start</button>
            `;

            // START APPLICATION PROCESS
            const startbtn = document.getElementById('start-application');
            startbtn.addEventListener('click', function() {
                const application_template = document.getElementById('start-application-template');
                const clone_template = application_template.content.cloneNode(true);
                container.innerHTML = "";
                container.appendChild(clone_template);

                // --- INITIALIZE DYNAMIC DOMELEMENTS INSIDE THE CLONE ---
                const submitbtn = document.getElementById('submitbtn');
                const warning = document.getElementById('warning');
                const province = document.getElementById('province');
                const city = document.getElementById('city');
                const barangay = document.getElementById('barangay');
                const college = document.getElementById('college');
                const choose_courses = document.getElementById('choose-courses');

                // DYNAMIC DATES & DROPDOWNS SETUP
                province.addEventListener('change', function() {
                    const selected = this.value;
                    city.innerHTML = "<option value=''>None</option>";
                    barangay.innerHTML = "<option value=''>None</option>"; // Reset barangay too

                    if(cities[selected]) {
                        cities[selected].forEach(function(item) {
                            const option = document.createElement('option');
                            option.value = item.toLowerCase().replace(/\s+/g, '_');
                            option.textContent = item;
                            city.appendChild(option);
                        });
                    }
                });

                city.addEventListener('change', function() {
                    const selected2 = this.value;
                    barangay.innerHTML = "<option value=''>None</option>";

                    if(barangay_list[selected2]) {
                        barangay_list[selected2].forEach(function(item) {
                            const option = document.createElement('option');
                            option.value = item.toLowerCase().replace(/\s+/g, '_');
                            option.textContent = item;
                            barangay.appendChild(option);
                        });
                    }
                });

                college.addEventListener('change', function() {
                    const selected = this.value;
                    choose_courses.innerHTML = '<option value="">None</option>';

                    if(courses[selected]) {
                        courses[selected].forEach(function(item) {
                            const option = document.createElement('option');
                            option.value = item.toLowerCase().replace(/\s+/g, '_');
                            option.textContent = item;
                            choose_courses.appendChild(option);
                        });
                    }
                });

                // SUBMIT AND VALIDATE THE FORM
                submitbtn.addEventListener('click', function() {
                    const formData = {
                        firstname: document.getElementById('firstname').value, 
                        middlename: document.getElementById('middlename').value,
                        lastname: document.getElementById('lastname').value,
                        contact_number: document.getElementById('contact').value, // Fixed from 'contact_number'
                        mothersname: document.getElementById('mothersname').value,
                        fathersname: document.getElementById('fathersname').value,
                        guardian: document.getElementById('guardian').value,
                        sex: document.getElementById('sex').value,
                        age: document.getElementById('age').value,
                        province: document.getElementById('province').value,
                        city: document.getElementById('city').value,
                        barangay: document.getElementById('barangay').value,
                        college: document.getElementById('college').value,
                        course: document.getElementById('choose-courses').value // FIXED: ID was 'choose-courses'
                    };

                    const checkEmptyFields = Object.values(formData).some(value => 
                        value === null || value === undefined || value.trim() === "" || value === "None" || value === "Sex"
                    );

                    if (checkEmptyFields) {
                        warning.textContent = "Missing Content!";
                    } else {
                        warning.textContent = "";
                        fetch('/apply_form', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(formData)
                        });

                        container.innerHTML = "<h1>SUCESSFULLY APPLIED</h1>"
                    }


                });
            });
        }
    });
});