<script>
    import axios from 'axios';
    import ModalUpdateGroups from '../components/ModalUpdateGroups.vue'
    import ModalCreateGroup from '../components/ModalCreateGroup.vue';

    export default {
        components: {ModalCreateGroup, ModalUpdateGroups},
        data() {
            return {
                data_groups: [],
            };
        },
        methods: {
            getDeleteGroupUser(deletedUser, groupId) {
                this.data_groups.find(x => x.id === groupId)['users'].splice(this.data_groups.findIndex(x => x.id === deletedUser), 1);
            },

            getUpdateGroupUser(updatedUser, groupId) {
                this.data_groups.find(x => x.id === groupId)['users'].push(updatedUser);
            },

            getUpdateGroupName(groupId, groupName) {
                let oldName = this.data_groups.find(x => x.id === groupId);
                let newGroup = Object.seal(oldName);
                newGroup.name = groupName;
            },

            getRoles() {
                const path = 'http://localhost:5000/groups';
                axios.get(path)
                    .then((res) => {
                        this.data_groups = res.data.data_groups;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },
            deleteGroup(group_id) {
                axios.post('http://localhost:5000/delete_group', {"group_id": group_id})
                    .then((res) => {
                        if (res.data.answer === 'ok') {
                            this.data_groups.splice(this.data_groups.findIndex(x => x.id === group_id), 1);
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
                <h1>Groups</h1>
                <hr>
                <br><br>
                <a href="./roles">
                    <button type="button" class="btn btn-success btn-sm">Roles</button>
                </a>
                <br><br>
                <a href="./users">
                    <button type="button" class="btn btn-success btn-sm">Users</button>
                </a>
                <br><br>
                <modal-create-group/>
                <br><br>
                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th scope="col">User</th>
                        <th scope="col">user in group</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="group in data_groups" :key="group">
                        <td>
                            <div>{{group.name}}</div>
                        </td>
                        <td>
                            <div type="hidden" v-for="user in group.users" :key="user">
                                {{user.name}}
                            </div>
                        </td>

                        <td>
                            <div class="btn-group" role="group">
                                <modal-update-groups v-on:updateGroupName="getUpdateGroupName"
                                                     v-on:updateGroupUser="getUpdateGroupUser"
                                                     v-on:deleteGroupUser="getDeleteGroupUser"
                                                     :group-id="group.id"/>
                                <button v-on:click="deleteGroup(group.id)" type="button" class="btn btn-danger btn-xs">
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
