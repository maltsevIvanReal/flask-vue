<script>
    import axios from 'axios';
    import ModalUpdateRoles from '../components/ModalUpdateRoles.vue'
    import ModalCreateRole from '../components/ModalCreateRole.vue'


    export default {
        components: {
            ModalCreateRole,
            ModalUpdateRoles
        },
        data() {
            return {
                data_roles: [],
            };
        },
        methods: {
            getUpdateRoleName(roleId, roleName) {
                let oldName = this.data_roles.find(x => x.id === roleId);
                let newRole = Object.seal(oldName);
                newRole.name = roleName;
            },

            getDeleteRoleGroup(deletedGroup, roleId) {
                this.data_roles.find(x => x.id === roleId)['groups'].splice(this.data_roles.findIndex(x => x.id === deletedGroup), 1);
            },

            getDeleteRoleUser(deletedUser, roleId) {
                this.data_roles.find(x => x.id === roleId)['users'].splice(this.data_roles.findIndex(x => x.id === deletedUser), 1);
            },

            getUpdateRoleGroup(updatedGroup, roleId) {
                this.data_roles.find(x => x.id === roleId)['groups'].push(updatedGroup);

            },

            getUpdateRoleUser(updatedUser, roleId) {
                this.data_roles.find(x => x.id === roleId)['users'].push(updatedUser);

            },

            getRoles() {
                const path = 'http://localhost:5000/roles';
                axios.get(path)
                    .then((res) => {
                        this.data_roles = res.data.data_roles;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },
            deleteRole(role_id) {
                axios.post('http://localhost:5000/delete_role', {"role_id": role_id})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                        this.data_roles.splice(this.data_roles.findIndex(x => x.id === role_id), 1);
                        } else {
                            alert('ERROR');
                        }
                    })
            },
        },
        created() {
            this.getRoles();
        },
    };
</script>
<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-10">
                <h1>Roles</h1>
                <hr>
                <br><br>
                <a href="./users">
                    <button type="button" class="btn btn-success btn-sm">Users</button>
                </a>
                <br><br>
                <a href="./groups">
                    <button type="button" class="btn btn-success btn-sm">Groups</button>
                </a>
                <br><br>
                <modal-create-role/>
                <br><br>
                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th scope="col">roles</th>
                        <th scope="col">user has roles</th>
                        <th scope="col">group has roles</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="role in data_roles" :key="role">
                        <td>
                            <div>{{role.name}}</div>
                        </td>
                        <td>
                            <div type="hidden" v-for="user in role.users" :key="user">
                                {{user.name}}
                            </div>
                        </td>
                        <td>
                            <div type="hidden" v-for="group in role.groups" :key="group">
                                {{group.name}}
                            </div>
                        </td>
                        <td>
                            <div class="btn-group" role="group">
                                <modal-update-roles v-on:updateRoleName="getUpdateRoleName"
                                                    v-on:updateRoleUser="getUpdateRoleUser"
                                                    v-on:updateRoleGroup="getUpdateRoleGroup"
                                                    v-on:deleteRoleUser="getDeleteRoleUser"
                                                    v-on:deleteRoleGroup="getDeleteRoleGroup"

                                                    :role-id="role.id"/>
                                <button v-on:click="deleteRole(role.id)" type="button" class="btn btn-danger btn-xs">
                                    Delete
                                </button>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
