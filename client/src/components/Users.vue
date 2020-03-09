<script>
    import axios from 'axios';
    import ModalUpdateUsers from '../components/ModalUpdateUsers.vue'
    import ModalCreateUser from '../components/ModalCreateUser.vue'


    export default {
        components: {
            ModalCreateUser,
            ModalUpdateUsers
        },
        data() {
            return {
                data_users: [],

            };
        },
        methods: {

            getUpdateUserName(userId, userName) {
                let oldName = this.data_users.find(x => x.id === userId);
                let newUser = Object.seal(oldName);
                newUser.name = userName;
            },

            getUpdatedGroup(updatedGroup, userId) {
                this.data_users.find(x => x.id === userId)['_groups'].push(updatedGroup);
            },

            getDeletedGroup(deletedGroup, userId) {
                this.data_users.find(x => x.id === userId)['_groups'].splice(this.data_users.findIndex(x => x.id === deletedGroup), 1);
            },

            getUpdatedRole(updatedRole, userId) {
                this.data_users.find(x => x.id === userId)['_roles'].push(updatedRole);
            },

            getDeleteRole(deletedRole, userId) {
                this.data_users.find(x => x.id === userId)['_roles'].splice(this.data_users.findIndex(x => x.id === deletedRole), 1);
            },


            getUsers() {
                const path = 'http://localhost:5000/users';
                axios.get(path)
                    .then((res) => {
                        this.data_users = res.data.data_users;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },
            deleteUser(user_id) {
                axios.post('http://localhost:5000/delete_user', {"id": user_id})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.data_users.splice(this.data_users.findIndex(x => x.id === user_id), 1);
                        } else {
                            alert('ERROR');
                        }
                    })
            },
        },
        created() {
            this.getUsers();
        },


    };

</script>

<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-10">
                <h1>Users</h1>
                <hr>
                <br><br>
                <a href="./roles">
                    <button type="button" class="btn btn-success btn-sm">Roles</button>
                </a>
                <br><br>
                <a href="./groups">

                    <button type="button" class="btn btn-success btn-sm">Groups</button>
                </a>
                <br><br>
                <modal-create-user/>
                <br><br>
                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th scope="col">User</th>
                        <th scope="col">user has role</th>
                        <th scope="col">user in group</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>


                    <tr v-for="item in data_users" :key="item">
                        <td>

                            <div>{{item.name}}</div>
                        </td>
                        <td>
                            <div type="hidden" v-for="role in item._roles" :key="role">
                                {{role.name}}
                            </div>
                        </td>
                        <td>
                            <div type="hidden" v-for="group in item._groups" :key="group">
                                {{group.name}}
                            </div>
                        </td>
                        <td>
                            <div class="btn-group" role="group">
                                <modal-update-users v-on:addNewUser="setNewUser"
                                                    v-on:updateUserName="getUpdateUserName"
                                                    v-on:deleteGroup="getDeletedGroup"
                                                    v-on:deleteRole="getDeleteRole"
                                                    v-on:updateRole="getUpdatedRole"
                                                    v-on:updateGroup="getUpdatedGroup"
                                                    :user-id="item.id"/>
                                <button type="button" v-on:click="deleteUser(item.id)" class="btn btn-danger btn-xs">
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
