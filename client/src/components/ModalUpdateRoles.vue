<template>
    <div>
        <b-button @click="show=true" v-on:click="getRoles" variant="primary">Update</b-button>

        <b-modal v-model="show">
            <div>
                <div v-if="role_name === 'employee' || role_name ==='administrator'">
                    <span>ROLE</span>
                    <b-form-input name="newname" :value="role_name" readonly></b-form-input>
                </div>
                <div v-else>
                    <span>ROLE</span>
                    <b-form-input v-model="role_name" name="newname"></b-form-input>
                    <b-button v-on:click="updateRoleName()" variant="success">change name</b-button>
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
                        <b-button v-on:click="updateRoleUser(selected_user.id)" variant="primary">Add user</b-button>
                    </b-form>
                    <span>USERS HAS ROLE</span>
                    <b-list-group v-for="user in role_users" :key="user">
                        <b-list-group-item class="d-flex justify-content-between align-items-center">
                            <b-icon v-on:click="deleteRoleUser(user.id)" icon="x-circle" scale="3"
                                    variant="danger"></b-icon>
                            {{user.name}}
                        </b-list-group-item>
                    </b-list-group>
                </div>

                <div>
                    <b-form inline>
                        <b-form-select
                                v-model="selected_group"
                                id="inline-form-custom-select-pref"
                                class="mb-2 mr-sm-2 mb-sm-0">
                            <option v-for="group in all_groups" :key="group" v-bind:value="{ id: group.id}">
                                {{group.name}}
                            </option>
                        </b-form-select>
                        <b-button v-on:click="updateGroupUser(selected_group.id)" variant="primary">Add group</b-button>
                    </b-form>
                    <span>GROUPS HAS ROLE</span>
                    <b-list-group v-for="group in role_groups" :key="group">
                        <b-list-group-item class="d-flex justify-content-between align-items-center">
                            <b-icon v-on:click="deleteRoleGroup(group.id)" icon="x-circle" scale="3"
                                    variant="danger"></b-icon>
                            {{group.name}}
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
        name: 'ModalUpdateRoles',
        props: ['roleId'],

        data() {
            return {
                selected_user: '',
                selected_group: '',
                role_id: 0,
                role_name: null,
                role_users: {},
                role_groups: {},
                all_groups: {},
                all_users: {},
                show: false,
            }
        },
        methods: {
            sendUpdateRoleName() {
                this.$emit('updateRoleName', this.roleId, this.role_name)
            },

            sendUpdateRoleGroup(updatedGroup) {
                this.$emit('updateRoleGroup', updatedGroup, this.role_id)
            },

            sendDeleteRoleGroup(deletedRoleId) {
                this.$emit('deleteRoleGroup', deletedRoleId, this.role_id)
            },

            sendDeleteRoleUser(deletedUserId) {
                this.$emit('deleteRoleUser', deletedUserId, this.role_id)
            },

            sendUpdateRoleUser(updatedUser) {
                this.$emit('updateRoleUser', updatedUser, this.role_id)
            },


            getRoles() {
                axios.post('http://localhost:5000/get_role', {"id": this.roleId})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.role_id = res.data.role.id;
                            this.role_name = res.data.role.name;
                            this.role_users = res.data.role.users;
                            this.role_groups = res.data.role.groups;
                            this.all_users = res.data.all_users;
                            this.all_groups = res.data.all_groups;

                        } else {
                            alert('ERROR');
                        }
                    })
            },
            updateRoleName() {
                axios.post('http://localhost:5000/update_role_name', {
                    "role_id": this.roleId,
                    "role_name": this.role_name
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.sendUpdateRoleName();
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            updateRoleUser(selected_user) {
                axios.post('http://localhost:5000/update_role_user', {
                    "role_id": this.role_id,
                    "user_id": selected_user
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            let newUser = this.all_users.find(x => x.id === selected_user);

                            if (!this.role_users.find(x => x.id === newUser.id)) {
                                this.role_users.push(newUser);
                                this.sendUpdateRoleUser(newUser);
                            }
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            deleteRoleUser(user_id) {
                axios.post('http://localhost:5000/delete_role_user', {
                    "user_id": user_id,
                    "role_id": this.role_id
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {

                            this.role_users.splice(this.role_users.findIndex(x => x.id === user_id), 1);
                            this.sendDeleteRoleUser(user_id);

                        } else {
                            alert('ERROR');
                        }
                    })
            }, updateGroupUser(selected_id) {
                axios.post('http://localhost:5000/update_role_group', {
                    "group_id": selected_id,
                    "role_id": this.role_id
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            let newGroup = this.all_groups.find(x => x.id === selected_id);

                            if (!this.role_groups.find(x => x.id === newGroup.id)) {
                                this.role_groups.push(newGroup);
                                this.sendUpdateRoleGroup(newGroup);
                            }


                        } else {
                            alert('ERROR');
                        }
                    })
            },
            deleteRoleGroup(group_id) {
                axios.post('http://localhost:5000/delete_group_role', {
                    "group_id": group_id,
                    "role_id": this.role_id
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {

                            this.role_groups.splice(this.role_groups.findIndex(x => x.id === group_id), 1);
                            this.sendDeleteRoleGroup(group_id);


                        } else {
                            alert('ERROR');
                        }
                    })
            },
        },
    }

</script>