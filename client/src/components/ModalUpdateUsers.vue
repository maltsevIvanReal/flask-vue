<template>
    <div>
        <b-button @click="show=true" v-on:click="getUser" variant="warning">Update</b-button>
        <b-modal v-model="show">
            <div>
                <div>
                    <span>USER NAME</span>
                    <b-form-input v-model="user_name"></b-form-input>
                    <b-button v-on:click="updateUserName()" variant="success">change name</b-button>
                </div>
                <div><span>USER HAS ROLES</span>
                    <b-form inline>
                        <b-form-select
                                v-model="selected_role"
                                id="inline-form-custom-select-pref"
                                class="mb-2 mr-sm-2 mb-sm-0">
                            <option v-for="role in all_roles" :key="role" v-bind:value="{ id: role.id}">{{role.name}}
                            </option>
                        </b-form-select>
                        <b-button v-on:click="updateUserRole(selected_role.id)" variant="primary">Add role</b-button>
                    </b-form>
                    <b-list-group v-for="role in user_roles" :key="role">
                        <b-list-group-item class="d-flex justify-content-between align-items-center">
                            <b-icon v-on:click="deleteUserRole(role.id)" icon="x-circle" scale="3"
                                    variant="danger"></b-icon>
                            {{role.name}}
                        </b-list-group-item>
                    </b-list-group>
                </div>
                <div><span>USER IN GROUPS</span>
                    <b-form inline>
                        <b-form-select v-model="selected_group"
                                       id="inline-form-custom-select-pref"
                                       class="mb-2 mr-sm-2 mb-sm-0">
                            <option v-for="group in all_groups" :key="group" v-bind:value="{id: group.id}">
                                {{group.name}}
                            </option>
                        </b-form-select>
                        <b-button v-on:click="updateUserGroup(selected_group.id)" variant="primary">Add group</b-button>
                    </b-form>
                    <b-list-group v-for="group in user_groups" :key="group">
                        <b-list-group-item class="d-flex justify-content-between align-items-center">
                            <b-icon v-on:click="deleteUserGroup(group.id)" icon="x-circle" scale="3"
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
        name: 'ModalUpdateUser',
        props: ['userId'],

        data() {
            return {
                selected_role: '',
                selected_group: '',
                user_id: 0,
                user_name: null,
                user_groups: [],
                user_roles: [],
                all_roles: [],
                all_groups: [],
                show: false,
            }
        },
        methods: {
            sendUpdateUserName() {
                this.$emit('updateUserName', this.userId, this.user_name)
            },

            sendUpdateGroup(updatedGroup) {
                this.$emit('updateGroup', updatedGroup, this.user_id)
            },

            sendDeletedGroup(deletedGroupId) {
                this.$emit('deleteGroup', deletedGroupId, this.user_id)
            },
            sendUpdateRole(updatedRole) {
                this.$emit('updateRole', updatedRole, this.user_id)
            },
            sendDeletedRole(deletedRoleId) {
                this.$emit('deleteRole', deletedRoleId, this.user_id)
            },

            getUser() {
                axios.post('http://localhost:5000/get_user',
                    {"id": this.userId})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.user_id = res.data.user.id;
                            this.user_name = res.data.user.name;
                            this.user_groups = res.data.user._groups;
                            this.user_roles = res.data.user._roles;
                            this.all_roles = res.data.all_roles;
                            this.all_groups = res.data.all_groups;
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            updateUserName() {
                axios.post('http://localhost:5000/update_user_name',
                    {"id": this.userId, "user_name": this.user_name})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.sendUpdateUserName();
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            updateUserRole(selected_role) {
                axios.post('http://localhost:5000/update_user_role', {
                    "id": this.userId,
                    "role_id": selected_role
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            let newRole = this.all_roles.find(x => x.id === selected_role);
                            if (!this.user_roles.find(x => x.id === newRole.id)) {
                                this.user_roles.push(newRole);
                                this.sendUpdateRole(newRole)
                            }
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            deleteUserRole(role_id) {
                axios.post('http://localhost:5000/delete_user_role', {
                    "id": this.userId,
                    "role_id": role_id
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.user_roles.splice(this.user_roles.findIndex(x => x.id === role_id), 1);
                            this.sendDeletedRole(role_id);
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            updateUserGroup(selected_group) {
                axios.post('http://localhost:5000/update_user_group', {
                    "id": this.userId,
                    "group_id": selected_group
                })
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            let newGroup = this.all_groups.find(x => x.id === selected_group);
                            if (!this.user_groups.find(x => x.id === newGroup.id)) {
                                this.user_groups.push(newGroup);
                                this.sendUpdateGroup(newGroup)
                            }
                        } else {
                            alert('ERROR');
                        }
                    })
            },
            deleteUserGroup(group_id) {
                axios.post('http://localhost:5000/delete_user_group',
                    {"id": this.userId, "group_id": group_id})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.user_groups.splice(this.user_groups.findIndex(x => x.id === group_id), 1);
                            this.sendDeletedGroup(group_id);

                        } else {
                            alert('ERROR');
                        }
                    })
            }
        },
    }

</script>