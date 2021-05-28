// VueJS Code for making an interactive web page to manage users in the system
Vue.component('usertable', {
    props: ['users', 'role'],
    template: `
    <table class="scoreboard">
        <tr>
            <th>username</th><th>email</th><th>role</th><th>effective start</th><th>effective end</th>
        </tr>
        <tr v-for="user in users" v-bind:key=user.username>
            <td>{{ user.username }}</td><td>{{ user.email }}</td><td>{{ user.role }}</td><td class="utcdate">{{ user.temp_start }}</td><td class="utcdate">{{ user.temp_end }}</td>
        </tr>
    </table>
    `
});

new Vue({
    el: '#root',
    data: {
        users: [],
        email: '',
        role: 'temp',
        username: '',
        password: '',
        confirm_password: '',
        temp_start: new Date(),
        temp_end: new Date(),
        page: 1,
        limit: 20,
        options: {
            headers: {
                "API-KEY": admin_token
            }
        },
    },
    methods: {
        updateUserTable: function() {
            axios
                .get("/api/users?page=" + this.page + '&limit=' + this.limit, this.options)
                .then((response) => {
                    this.users = response.data;
                })
                .catch(function (error) {
                    console.log("Error !!!:");
                    console.log(error);
                });
        },
        createUser: function() {   
            axios
                .post("/api/users/" + this.username,
                    {
                        "email": this.email,
                        "role": this.role,
                        "password": this.password,
                        "temp_start": (new Date(this.temp_start)).getTime() / 1000,
                        "temp_end": (new Date(this.temp_end)).getTime() / 1000
                    },
                    this.options
                )
                .then((response) => {
                    console.log(response.data);
                })
                .then(() => {this.updateUserTable();})
                .catch(function (error) {
                    console.log("Error !!!:");
                    console.log(error);
                });
            this.role = 'temp';
            this.username = '';
            this.email = '';
            this.password = '';
            this.confirm_password = '';
            this.temp_start = new Date();
            this.temp_end = new Date();
        },
        updateUser: function() {
            axios
                .put("/api/users/" + this.username,
                    {
                        "email": this.email,
                        "role": this.role,
                        "password": this.password,
                        "temp_start": (new Date(this.temp_start)).getTime() / 1000,
                        "temp_end": (new Date(this.temp_end)).getTime() / 1000
                    },
                    this.options
                )
                .then((response) => {
                    console.log(response.data);
                })
                .then(() => {this.updateUserTable();})
                .catch(function (error) {
                    console.log("Error !!!:");
                    console.log(error);
                });
            this.role = 'temp';
            this.username = '';
            this.email = '';
            this.password = '';
            this.confirm_password = '';
            this.temp_start = new Date();
            this.temp_end = new Date();
        },
        deleteUser: function() {
            axios
                .delete("/api/users/" + this.username, this.options)
                .then((response) => {
                    console.log(response.data);
                })
                .then(() => {this.updateUserTable();})
                .catch(function (error) {
                    console.log("Error !!!:");
                    console.log(error);
                });
            this.role = 'temp';
            this.username = '';
            this.email = '';
            this.password = '';
            this.confirm_password = '';
            this.temp_start = new Date();
            this.temp_end = new Date();
        },
    },
    mounted: function () {
        this.updateUserTable()
    }
});
