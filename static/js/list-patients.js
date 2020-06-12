Vue.use(Vuetable);
new Vue({
    el: '#app',
    components: {
        'vuetable-pagination': Vuetable.VuetablePagination
    },
    data: {
        userProfileImg: '',
        addressUser: '',
        fields: [
            {
                name: 'document_type',
                title: 'Tipo documento',
                titleClass: 'center aligned',
                dataClass: 'center aligned'
            },
            {
                name: 'document_number',
                title: 'Número documento',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            }, 
            {
                name: 'full_name',
                title: 'Nombre',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'age',
                title: 'Edad',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'gender',
                title: 'Sexo',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'address',
                title: 'Dirección',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'photo',
                visible: false
            },
            '__slot:actions'
        ]
    },
    methods: {
        onPaginationData(paginationData) {
            this.$refs.pagination.setPaginationData(paginationData)
        },
        onChangePage(page) {
            this.$refs.vuetable.changePage(page)
        },
        generatePath(photo, address) {
            this.userProfileImg = `data:img/png;base64,${photo}`;
            this.addressUser = address;
            $('.ui.modal').modal('show').modal({
                onVisible: function () {
                    let input = document.getElementById("search-address-input");
                    google.maps.event.trigger(input, "focus", {});
                    google.maps.event.trigger(input, "keydown", {keyCode: 13});
                  },
            });
        },
        deleteRow(rowData) {
            alert("You clicked delete on" + JSON.stringify(rowData))
        }
    }
});