// 文件路径: static/js/login.js
// 这是一个完全修正后的版本，请用它替换您原来的文件内容。

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
                        $("#registeform").data('bootstrapValidator').destroy();
                        $('#registeform').data('bootstrapValidator', null);
                    } else {
                        // *** 关键修复开始 ***
                        alert(result['msg']); // 提示注册成功

                        // 1. 使用正确的ID ('#register-modal') 来隐藏注册弹窗
                        $('#register-modal').modal('hide');

                        // 2. 监听注册弹窗“完全隐藏后”的事件
                        $('#register-modal').on('hidden.bs.modal', function (e) {
                            // 3. 在它完全隐藏后，再用正确的ID ('#login-modal') 安全地显示登录弹窗
                            //    这可以避免两个弹窗的蒙层冲突
                            $('#login-modal').modal('show');
                            // 4. 解除本次事件绑定，避免下次重复触发
                            $(this).off('hidden.bs.modal');
                        });
                        // *** 关键修复结束 ***
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
                        alert(result['msg']); // 登录失败
                        $("#loginform").data('bootstrapValidator').destroy();
                        $('#loginform').data('bootstrapValidator', null);
                    } else {
                        // 登录成功后刷新当前页面
                        window.location.reload();
                    }
                },
            })
        }
    });

    // 退出
    $("#logout").on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: '/logout',
            type: 'get',
            dataType: 'json',
            success: function (res) {
                if (res["valid"] == '1') {
                    window.location.href = '/';
                } else {
                    alert(res["msg"]);
                }
            }
        })
    });
});
