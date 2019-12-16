API_END_POINT = 'http://localhost:8000/list1/';

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let [k,v] = el.split('=');
      cookie[k.trim()] = v;
    })
    return cookie[name];
}

var app = angular.module("myApp", ['ngRoute']);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

    $locationProvider.html5Mode(true);
    $routeProvider
        .when('/', {
            templateUrl: '/views/login.html',
            controller: 'loginController'
        }) 
        .when('/main', {
            templateUrl: '/views/main.html',
            controller: 'mainPage'
        })
        .when('/group/:groupId', {
            templateUrl: '/views/group.html',
            controller: 'groupView',
        });
}]);

app.controller("loginController", function($scope, $http, $window, $location){
    $scope.loginQuery = function(uname, pass){
        if(uname==="" || pass==="" || uname == null || pass==null){
            alert("All fields are necessary.")
        } else {
            $http({
                method: 'post',
                url: API_END_POINT.concat('login'),
                data: {'user_id':uname, 'password':pass}
            })
            .then(function(response){
                console.log(response.data);

                var date = new Date();
                date.setTime(+ date + 1200000)

                $window.document.cookie = 'token=Bearer ' + encodeURIComponent(response.data.token) + '; path=/; expires=' + date.toGMTString() + ";";
                $location.path(response.data.path);
            })
            .catch(function(error){
                alert("User Details invalid!");
            })    
        }
    }

    $scope.signup = function(userid, pass, name){
        $http({
            method: 'POST',
            url: API_END_POINT.concat('useradd'),
            data: {'name':name, 'user_id':userid, 'password':pass, 'active':true}
        })
        .then(function(response) {
            console.log(response.data.message);
            alert(response.data.message);
        })
    }
});



/* ======================== Main Page ======================== */



app.controller("mainPage", function($scope, $http, $location) {

    $http({
        method: 'GET',
        url: 'http://localhost:8000/list1/groupget/',
        headers : {
            'Authorization' : getCookie('token')
        }
    })
    .then(function(response) {
        $scope.taskGroups = response.data;
        console.log($scope.taskGroups)
    })  


    $scope.addGroup = function(groupName){
        $http({
            method: 'POST',
            url : API_END_POINT.concat('groupadd'),
            headers : {
                'Authorization' : getCookie('token')
            },
            data : {'group_title': groupName}
        })
        .then(function(response){
            console.log(response);
            if(response.status == 201){
                alert("Group Added");
                $http({
                    method: 'GET',
                    url: 'http://localhost:8000/list1/groupget/',
                    headers : {
                        'Authorization' : getCookie('token')
                    }
                })
                .then(function(response) {
                    $scope.taskGroups = response.data;
                    console.log($scope.taskGroups)
                })
            }
        })
    }

    $scope.openTaskGroup = function(taskGroupId, taskGroupTitle){
        $location.path("/group/"+taskGroupId);
    }
})


/* ======================== Group View Page ======================== */


app.controller("groupView", function($scope, $http, $routeParams, $location, $window){
    $scope.groupId = $routeParams.groupId;

    $http({
        method: 'GET',
        url: 'http://localhost:8000/list1/taskget/' + $scope.groupId + "/",
        headers : {
            'Authorization' : getCookie('token')
        },
    })
    .then(function(response) {
        $scope.tasks = response.data;
        console.log($scope.tasks)
    })

    $scope.addTask = function(desc){
        $http({
            method:'POST',
            url: API_END_POINT.concat('taskadd/' + $scope.groupId + "/"),
            data: {
                'task_description':desc
            }
        })
        .success(function(response){
            console.log(response.message);

            $http({
                method: 'GET',
                url: 'http://localhost:8000/list1/taskget/' + $scope.groupId + "/",
                headers : {
                    'Authorization' : getCookie('token')
                }
            })
            .then(function(response) {
                $scope.tasks = response.data;
                console.log($scope.tasks)
            })
        })
    }

    $scope.removeTask = function(taskId){
        $http({
            method: 'DELETE',
            url: 'http://localhost:8000/list1/taskdelete',
            headers : {
                'Authorization' : getCookie('token')
            },
            data: {
                'task_id': taskId
            }
        })
        .then(function(response) {
            console.log(response.message)
            $http({
                method: 'GET',
                url: 'http://localhost:8000/list1/taskget/' + $scope.groupId + "/",
                headers : {
                    'Authorization' : getCookie('token')
                },
            })
            .then(function(response) {
                $scope.tasks = response.data;
                console.log($scope.tasks)
            })
        })
    }

    $scope.taskStatusChange = function(taskId, status){
        $http({
            method: 'PATCH',
            url: 'http://localhost:8000/list1/taskstatuschange',
            data: {
                'task_id': taskId,
                'task_status': status
            }
        })
        .then(function(response) {
            console.log(response.message)
            $http({
                method: 'GET',
                url: 'http://localhost:8000/list1/taskget/' + $scope.groupId + "/",
                headers : {
                    'Authorization' : getCookie('token')
                },
            })
            .then(function(response) {
                $scope.tasks = response.data;
                console.log($scope.tasks)
            })
        })
    }

    $scope.deleteGroup = function(){
        var groupId = $scope.groupId;
        $http({
            method: "DELETE",
            url: 'http://localhost:8000/list1/groupdelete',
            headers : {
                'Authorization' : getCookie('token')
            },
            data: {
                'group_id': groupId
            }
        })
        .then(function(response) {
            alert(response.data.message);
            $window.document.getElementsByClassName("modal-backdrop")[0].style.display = "none";
            $location.path("/main");
        })
    }
});