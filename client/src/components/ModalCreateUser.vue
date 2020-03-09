<template>
    <div>
        <b-button @click="show=true" variant="success" size="sm">Add new user</b-button>
        <b-modal v-model="show">
            <div>
                <div>
                    <span>USER NAME</span>
                    <b-form-input id="user_name" required v-model="user_name"></b-form-input>
                    <b-button v-on:click="addUser(user_name)" variant="success">add user</b-button>
                </div>
            </div>
        </b-modal>
    </div>
</template>
<script>
    import axios from 'axios';

    export default {
        name: 'ModalCreateUser',
        data() {
            return {
                user_id: 0,
                user_name: null,
                show: false,
                new_user: {}
            }
        },
        methods: {
            sendAddedUser(user) {
                this.$emit('addNewUser', user);
            },
            addUser() {
                if (document.getElementById('user_name').validity.valid) {
                    axios.post('http://localhost:5000/add_user', {"user_name": this.user_name})
                        .then((res) => {
                            if (res.data.answer === 'ok') {
                                this.new_user = res.data.added_user;
                                this.sendAddedUser(this.new_user);

                            } else {
                                alert('ERROR');
                            }
                        })
                }
            }
        },
    }

</script>