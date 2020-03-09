<template>
    <div>
        <b-button @click="show=true" v-on:click="getUser" variant="primary">Update</b-button>
        <b-modal v-model="show">
            <div>
                <div>
                    <span>GROUP NAME</span>
                    <b-form-input name="newname" v-model="group_name" placeholder="Enter your name"></b-form-input>
                    <b-button v-on:click="updateGroupName()" variant="success">change name</b-button>
                </div>

                <div>
                    <b-form inline>
                        <b-form-select
                                v-model="selected_user"
                                id="inline-form-custom-select-pref"
                                class="mb-2 mr-sm-2 mb-sm-0">
                            <option v-for="user in all_users" :key="user" v-bind:value="{ id: user.id}">{{user.name}}
                            </option>
                        </b-form-select>
                        <b-button v-on:click="addUserGroup(selected_user.id)" variant="primary">Add user in group
                        </b-button>
                    </b-form>
                    <span>USERS IN GROUP</span>
                    <b-list-group v-for="user in group_users" :key="user">
                        <b-list-group-item class="d-flex justify-content-between align-items-center">
                            <b-icon v-on:click="deleteGroupUser(user.id)" icon="x-circle" scale="3"
                                    variant="danger"></b-icon>
                            {{user.name}}
                        </b-list-group-item>
                    </b-list-group>
                </div>
            </div>
        </b-modal>
    </div>
</template>
<script>
    import axios from 'axios';

    export default {
        name: 'ModalUpdateGroups',
        props: ['groupId'],

        data() {
            return {
                selected_user: '',
                group_id: 0,
                group_name: null,
                group_users: {},
                all_groups: {},
                all_users: {},
                show: false,
            }
        },
        methods: {

            sendDeleteGroupUser(deletedUserId) {
                this.$emit('deleteGroupUser', deletedUserId, this.group_id)
            },

            sendUpdateGroupUser(updatedUser) {
                this.$emit('updateGroupUser', updatedUser, this.group_id)
            },

            sendUpdateGroupName() {
                this.$emit('updateGroupName', this.groupId, this.group_name)
            },


            getUser() {
                axios.post('http://localhost:5000/get_group', {"id": this.groupId})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.group_id = res.data.group.id;
                            this.group_name = res.data.group.name;
                            this.group_users = res.data.group.users;
                            this.all_users = res.data.all_users;
                            this.all_groups = res.data.all_groups;
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            updateGroupName() {
                axios.post('http://localhost:5000/update_group_name', {
                    "group_id": this.groupId,
                    'group_name': this.group_name
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.sendUpdateGroupName();
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            addUserGroup(selected_id) {
                axios.post('http://localhost:5000/update_group_user', {
                    "user_id": selected_id,
                    "group_id": this.group_id
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            let newUser = this.all_users.find(x => x.id === selected_id);
                            if (!this.group_users.find(x => x.id === newUser.id)) {
                                this.group_users.push(newUser);
                                this.sendUpdateGroupUser(newUser);
                            }
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            deleteGroupUser(user_id) {
                axios.post('http://localhost:5000/delete_group_user', {
                    "user_id": user_id,
                    "group_id": this.group_id
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.group_users.splice(this.group_users.findIndex(x => x.id === user_id), 1);
                            this.sendDeleteGroupUser(user_id);
                        } else {
                            alert('ERROR');
                        }
                    })
            },
        },
    }

</script>