const ListRendering = {
    data() {
        return {
            profile_status: []
        }
    },
    mounted() {
        //get request
        //use results
        axios.get('/profile_status/')
            .then(function (response) {
                // handle success
                myapp.profile_status = response.data.profile_status;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        setInterval(()=>{
            axios.get('/profile_status/')
            .then(function (response) {
                // handle success
                myapp.profile_status = response.data.profile_status;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

myapp = Vue.createApp(ListRendering).mount('#list-rendering')
