$(document).ready(function () {

    // 注册
    $('#registe-btn').on('click', function () {
        // --- 注册表单的验证逻辑保持不变 ---
        $('#registeform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: { message: '用户名不能为空' },
                        stringLength: { min: 6, max: 15, message: '用户名长度必须在6到15位之间' },
                        regexp: { regexp: /^[a-zA-Z0-9_\.]+$/, message: '用户名只能包含大写、小写、数字和下画线' },
                        different: { field: 'password', message: '用户名不能与密码相同' }
                    }
                },
                email: {
                    validators: {
                        notEmpty: { message: '邮箱不能为空' },
                        emailAddress: { message: '无效的邮箱地址' }
                    }
                },
                password: {
                    validators: {
                        notEmpty: { message: '密码不能为空' },
                        identical: { field: 'confirmPassword', message: '与确认密码不一致' },
                        different: { field: 'username', message: '密码不能与用户名相同' }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: { message: '确认密码不能为空' },
                        identical: { field: 'password', message: '与密码不一致' },
                        different: { field: 'username', message: '确认密码不能与用户名相同' }
                    }
                }
            }
        });
        var validator = $('#registeform').data("bootstrapValidator");
        validator.validate();
        if (validator.isValid()) {
            $.ajax({
                type: 'post',
                url: '/register', // 后端注册接口
                data: $('#registeform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg']); // 注册失败，提示错误信息
                        // 销毁验证，以便下次可以重新验证
                        $("#registeform").data('bootstrapValidator').destroy();
                        $('#registeform').data('bootstrapValidator', null);
                    } else {
                        // *** 修改开始: 注册成功后直接跳转到登录模态框 ***
                        alert(result['msg']); // 提示注册成功
                        $('#register').modal('hide'); // 关闭注册模态框
                        $('#login').modal('show'); // 打开登录模态框
                        // *** 修改结束 ***
                    }
                },
            })
        }
    });

    // 登录
    $('#login-btn').on('click', function () {
        // --- 登录表单的验证逻辑保持不变 ---
        $('#loginform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    validators: {
                        notEmpty: { message: '用户名不能为空' },
                        stringLength: { min: 6, max: 15, message: '用户名长度必须在6到15位之间' },
                        regexp: { regexp: /^[a-zA-Z0-9_\.]+$/, message: '用户名只能包含大写、小写、数字和下画线' }
                    }
                },
                password: {
                    validators: {
                        notEmpty: { message: '密码不能为空' },
                        different: { field: 'username', message: '密码不能与用户名相同' }
                    }
                }
            }
        });
        var validator = $('#loginform').data("bootstrapValidator");
        validator.validate();
        if (validator.isValid()) {
            $.ajax({
                type: 'post',
                url: '/login', // 后端登录接口
                data: $('#loginform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg']); // 登录失败，提示错误信息
                        // 销毁验证
                        $("#loginform").data('bootstrapValidator').destroy();
                        $('#loginform').data('bootstrapValidator', null);
                    } else {
                        // *** 修改开始: 登录成功后刷新当前页面 ***
                        // 后端会设置好 session，刷新后导航栏会显示用户名
                        window.location.reload();
                        // *** 修改结束 ***
                    }
                },
            })
        }
    });

    // 退出
    $("#logout").on('click', function (e) {
        e.preventDefault(); // 阻止链接的默认跳转行为
        $.ajax({
            url: '/logout',
            type: 'get',
            dataType: 'json',
            success: function (res) {
                if (res["valid"] == '1') {
                    // 退出成功，刷新页面
                    window.location.href = '/';
                } else {
                    alert(res["msg"]);
                }
            }
        })
    });
});
