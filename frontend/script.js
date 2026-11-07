const API_URL = "http://YOUR_EC2_PUBLIC_IP:5000";

const form = document.getElementById("peopleForm");

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const person = {

        name: document.getElementById("name").value,

        age: document.getElementById("age").value,

        email: document.getElementById("email").value,

        city: document.getElementById("city").value

    };

    try {

        const response = await fetch(`${API_URL}/people`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(person)

        });

        const result = await response.json();

        document.getElementById("message").innerText =
            result.message || result.error || "Request failed";

        if (response.ok) {

            form.reset();

        }

    } catch (error) {

        document.getElementById("message").innerText =
            "Error connecting to backend";

        console.error(error);

    }

});


async function getPeople() {

    try {

        const response = await fetch(`${API_URL}/people`);

        if (!response.ok) {
            throw new Error("Unable to retrieve people");
        }

        const people = await response.json();

        const list = document.getElementById("peopleList");

        list.innerHTML = "";

        people.forEach(person => {

            const div = document.createElement("div");

            div.className = "person";

            div.innerText =
                `Name: ${person.name} | Age: ${person.age} | Email: ${person.email} | City: ${person.city}`;

            list.appendChild(div);

        });

    } catch (error) {

        console.error(error);

        document.getElementById("message").innerText =
            "Unable to retrieve records";

    }

}
