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

    $routeProvider
        .when('/', {
            templateUrl: '/views/login.html',
            controller: 'loginController'
        }) 
        .when('/main', {
            templateUrl: '/views/main.html',
            controller: 'mainPage'
        })
        .when('/resetPassword', {
            templateUrl: 'views/reset.html',
            controller: 'resetPass'
        })
        .when('/group/:groupId', {
            templateUrl: '/views/group.html',
            controller: 'groupView',
        });
}]);

app.controller("loginController", function($scope, $http, $window, $location){
    $window.$("input[data-toggle='tooltip']").on('focus', function() {
        $(this).tooltip('show');
    });
    
    $window.$("input[data-toggle='tooltip']").on('blur', function() {
        $(this).tooltip('hide');
    });

    if(getCookie('token')){
        $location.path('/main');
    }
    
    $scope.loginQuery = function(uname, pass){
        if(uname==="" || pass==="" || uname == null || pass==null){
            $window.toastr.error("All fields are necessary.")
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
                $window.toastr.error("User Details invalid!");
            })    
        }
    }

    $scope.signup = function(userid, pass, repass, name){
        if(pass != repass){
            $window.toastr.error("Both Passwords don't match")
            $scope.pass = "";
            $scope.repass = "";
        } else {
            let passRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,16}$/;
            if(pass.match(passRegex)){
                $http({
                    method: 'POST',
                    url: API_END_POINT.concat('useradd'),
                    data: {'name':name, 'user_id':userid, 'password':pass, 'active':true}
                })
                .then(function(response) {
                    console.log(response.data.message);
                    $window.$("#modalRegisterForm").modal("hide");
                    $window.toastr.success(response.data.message, "Welcome to To-Do");
                })
            }
            else {
                $window.toastr.error("Password doesn't match the type requested!")
                $scope.pass = "";
                $scope.repass = "";
            }
            
        }
    }

});



/* ======================== Main Page ======================== */



app.controller("mainPage", function($scope, $http, $location, $window) {

    if(getCookie('token') == "" || getCookie('token') == null){
        $location.path('/');
        $window.toastr.error('Please Log in Again','User Timed-Out')
    }

    $http({
        method: 'GET',
        url: API_END_POINT.concat('groupget/'),
        headers : {
            'Authorization' : getCookie('token')
        }
    })
    .then(function(response) {
        $scope.groupsPersonal = response.data.owner;
        $scope.groupsOther = response.data.not_owner;
        console.log($scope.groupsPersonal);
        console.log($scope.groupsOther);
    })  


    $scope.addGroup = function(groupName){
        if(groupName === "" || groupName ==  null){
            $window.toastr.error("Group name can't be blank");
        }
        else{
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
                    $window.$("#modalAddGroup").modal("hide");
                    $window.toastr.success("Group added!!!!");
                    $http({
                        method: 'GET',
                        url: API_END_POINT.concat('groupget/'),
                        headers : {
                            'Authorization' : getCookie('token')
                        }
                    })
                    .then(function(response) {
                        $scope.groupsPersonal = response.data.owner;
                        $scope.groupsOther = response.data.not_owner;
                        console.log($scope.groupsPersonal);
                        console.log($scope.groupsOther);
                    })
                }
            })
        }
    }

    $scope.openTaskGroup = function(taskGroupId, taskGroupTitle){
        $location.path("/group/"+taskGroupId);
    }

    $scope.signOut = function() {
        $window.document.cookie = "token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT"
        $location.path("/");
        $window.toastr.success("Logged out successfully");
    }
})


/* ======================== Group View Page ======================== */


app.controller("groupView", function($scope, $http, $routeParams, $location, $window){
    $scope.groupId = $routeParams.groupId;
    $scope.shareAllView = true;
    var token = getCookie('token');

    $http({
        method: 'GET',
        url: API_END_POINT.concat('taskget/' + $scope.groupId + "/"),
        headers : {
            'Authorization' : token
        }
    })
    .then(function(response) {
        $scope.tasks = response.data;
        console.log($scope.tasks)
    })

    $http({
        method: 'GET',
        url: API_END_POINT.concat('userget/'),
        headers : {
            'Authorization' : getCookie('token')
        }
    })
    .then(function(response) {
        $scope.listOfUsers = response.data.users; 
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
            $window.$("#addTask").modal("hide");
            $window.toastr.success(response.message);

            $http({
                method: 'GET',
                url: API_END_POINT + 'taskget/' + $scope.groupId + "/",
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
            url: API_END_POINT + 'taskdelete',
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
                url: API_END_POINT + 'taskget/' + $scope.groupId + "/",
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
            url: API_END_POINT + 'taskstatuschange',
            data: {
                'task_id': taskId,
                'task_status': status
            }
        })
        .then(function(response) {
            console.log(response.data.message)
            $http({
                method: 'GET',
                url: API_END_POINT + 'taskget/' + $scope.groupId + "/",
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
            url: API_END_POINT + 'groupdelete',
            headers : {
                'Authorization' : getCookie('token')
            },
            data: {
                'group_id': groupId
            }
        })
        .then(function(response) {
            $window.document.getElementsByClassName("modal-backdrop")[0].remove();
            $location.path("/main");
            $window.toastr.success("Task List named " + response.data.title + " removed!", "Task List Removed");
        })
        .catch(function(response){
            $window.$("#deleteGroup").modal("hide");
            window.toastr.error(response.data.message);
        })
    }

    $scope.shareForAllView = function(){
        $scope.shareAllView = true;
    }
    $scope.shareForSpecificView = function(){
        $scope.shareAllView = false;
    }

    $scope.enableShareForAll = function(){
        var groupId = $scope.groupId;
        var allChecked = $scope.shareAllView;

        $http({
            method: "POST",
            url: API_END_POINT + 'groupshare',
            headers : {
                'Authorization': getCookie('token')
            },
            data: {
                'group_id': groupId,
                'all_checked': allChecked
            }
        })
        .then(function(response) {
            if(response.status == 202){
                $window.$("#shareGroup").modal("hide");
                //$window.document.getElementsByClassName("modal-backdrop")[0].remove();
                $window.toastr.success("Sharing enabled to all");
            }
            else {
                $window.toastr.error("Some error occured. Please check the console.");
            }
        })
        .catch(function(response){
            $window.$("#shareGroup").modal("hide");
            $window.toastr.error(response.data.message);
        })
    }

    $scope.enableShareForSome = function() {
        var shareWithSomeTable = $window.$("input[name=sharedWithSpecificUsers]:checked")
        var shareAccessGiven = [];
        $.each(shareWithSomeTable, function(){
            shareAccessGiven.push($(this).val());
        })
        var groupId = $scope.groupId;
        $http({
            method: 'POST',
            url: API_END_POINT + 'groupshare/',
            headers : {
                'Authorization': getCookie('token')
            },
            data: {
                'all_checked': false,
                'group_id': groupId,
                'user_ids': shareAccessGiven
            }
        })
        .then(function(response) {
            console.log(response);
            if(response.status == 202){
                $window.$("#shareGroup").modal("hide");
                $window.toastr.success("Sharing enabled to selected users");
            } else {
                $window.toastr.error("Some error occured. Please check the console.");
            }
        })
        .catch(function(response){
            $window.$("#shareGroup").modal("hide");
            $window.toastr.error(response.data.message);
        })
        
    }
    $scope.signOut = function() {
        $window.document.cookie = "token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT"
        $location.path("/");
        $window.toastr.success("Logged out successfully");
    }

});

app.controller("resetPass", function($scope, $http, $location, $window){
    $window.$("input[data-toggle='tooltip']").on('focus', function() {
        $(this).tooltip('show');
    });
    
    $window.$("input[data-toggle='tooltip']").on('blur', function() {
        $(this).tooltip('hide');
    });
    
    $scope.changePassword = function(){
        if($scope.pass == $scope.repass) {
            let passRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,8}$/;
            if(pass.match(passRegex)){
                var pass  = $scope.pass;
                $http({
                    method: 'PATCH',
                    url: API_END_POINT + 'passchange/',
                    headers : {
                        'Authorization': getCookie('token')
                    },
                    data : {
                        'password': pass
                    }
                })
                .then(function(response){
                    $location.path("/main");
                    $window.toastr.success("Password Successfully Changed")
                })
                .catch(function(response) {
                    $location.path("/main");
                    $window.toastr.error("You are not authorized to change password for this user!")
                })
            }
            else{
                $window.toastr.error("Password doesn't match the type requested!")
                $scope.pass = "";
                $scope.repass = "";
            }
        }
        else{
            $window.toastr.error("Both Passwords don't match")
            $scope.pass = "";
            $scope.repass = "";
        }
    }
    
})