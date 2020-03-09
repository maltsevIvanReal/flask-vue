<template>
    <div>
        <b-button @click="show=true" variant="success" size="sm">Add new group</b-button>
        <b-modal v-model="show">
            <div>
                <div>
                    <span>GROUP NAME</span>
                    <b-form-input id="group_name" required v-model="group_name"></b-form-input>
                    <b-button v-on:click="addGroup(group_name)" variant="success">add group</b-button>
                </div>
            </div>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'ModalCreateGroup',

        data() {
            return {
                group_id: 0,
                group_name: null,
                show: false,
            }
        },
        methods: {
            addGroup(group_name) {
                if (document.getElementById('group_name').validity.valid) {
                    axios.post('http://localhost:5000/add_group', {"group_name": group_name})
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