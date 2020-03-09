<template>
    <div>
        <b-button @click="show=true" variant="success" size="sm">Add new role</b-button>
        <b-modal v-model="show">
            <div>
                <div>
                    <span>ROLE NAME</span>
                    <b-form-input id="role_name" required v-model="role_name"></b-form-input>
                    <b-button v-on:click="addRole(role_name)" variant="success">add role</b-button>
                </div>
            </div>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'ModalCreateRole',
        data() {
            return {
                role_id: 0,
                role_name: null,
                show: false,
            }
        },
        methods: {
            addRole(role_name) {
                if (document.getElementById('role_name').validity.valid) {
                    axios.post('http://localhost:5000/add_role', {"role_name": role_name})
                        .then((res) => {
                            if (res.data.answer === 'ok') {
                                console.log("ok")
                            } else {
                                alert('ERROR');
                            }
                        })
                }
            }
        },
    }

</script>