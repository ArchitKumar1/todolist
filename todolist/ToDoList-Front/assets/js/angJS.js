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
            method: 'post',
            url: API_END_POINT.concat('useradd'),
            data: {'name':name, 'user_id':userid, 'password':pass, 'active':true}
        })
        .then(function(response) {
            console.log(response.data.message);
            alert(response.data.message);
        })
    }
});



/* ======================== Main Page ======================= */



app.controller("mainPage", function($scope, $http, $window, $location) {

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

    /* $scope.taskGroups = [
        {'taskGroupName' : 'Wubba Lubba Dub Dub', 'tasklist_id' : '1192'}, 
        {'taskGroupName' : 'Study' , 'tasklist_id' : '9910'},
        {'taskGroupName' : 'Work' , 'tasklist_id' : '0193'},
        {'taskGroupName' : 'Dance' , 'tasklist_id' : '00192'},
    ] */

    $scope.addGroup = function(groupName){
        $http({
            method: 'POST',
            url : API_END_POINT.concat('groupadd'),
            headers : {
                'Authorization' : getCookie('token')
            },
            data : {'group_title': groupName, 'group_id': 'blindw'}
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

    $scope.openTaskGroup = function(taskGroupId){
        $location.path("/group/"+taskGroupId);
    }
})




app.controller("groupView", function($scope, $http, $window, $routeParams){
    $scope.groupId = $routeParams.groupId;
    console.log($scope.groupId);
    $scope.defaultV = true;
    $scope.addItemV = false;

    $scope.items = 
    [
        {
            task : "Walk Back to Home",
            task_id: 23454
        }
    ];

    $scope.addItemView = function(){
        $scope.defaultV = false;
        $scope.addItemV = true;
    }

    $scope.removeTask = function(itemId){
        console.log("remove task : ",itemId);
    }

    $scope.addTask = function(id, desc, groupId, taskStatus){
        if (!taskStatus){
            taskStatus = 0
        }
        $http({
            method:'POST',
            url: API_END_POINT.concat('task/'),
            data: {'taskDescription':id, 'taskId':desc, 'taskGroupId':groupId, 'taskStatus':taskStatus}
        })
        .success(function(response){
            console.log(response);
        })
    }
});