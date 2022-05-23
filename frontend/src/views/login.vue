<template>
  <div class="login">
    <div
      v-for="(project, num) in allCirle"
      :key="num"
      class="bg_circle"
      :class="[project.class]"
    ></div>
    <div class="login-box">
      <div class="login-container">
        <t-loading style="margin: auto" :loading="loading" showOverlay>
          <t-form
            :data="formData"
            ref="form"
            @submit="onSubmit"
            :rules="rules"
            :labelWidth="0"
            :disabled="formdisabled"
          >
            <t-form-item name="title">
              <h2 style="margin: auto">登录</h2>
            </t-form-item>
            <t-form-item name="account">
              <t-input
                clearable
                v-model="formData.account"
                placeholder="请输入账户名"
              >
                <desktop-icon slot="prefix-icon"></desktop-icon>
              </t-input>
            </t-form-item>
            <t-form-item name="password">
              <t-input
                type="password"
                clearable
                v-model="formData.password"
                placeholder="请输入密码"
              >
                <lock-on-icon slot="prefix-icon"></lock-on-icon>
              </t-input>
            </t-form-item>
            <t-form-item>
              <t-button
                class="submit-button"
                theme="primary"
                shape="circle"
                type="submit"
              >
                <icon-font name="arrow-right" />
              </t-button>
              <a style="margin-left: auto; color: #2e81f9" @click="OnUserIn"
                >游客登录 ></a
              >
            </t-form-item>
          </t-form>
        </t-loading>
      </div>
    </div>
  </div>
</template>

<script>
import { DesktopIcon, LockOnIcon, IconFont } from "tdesign-icons-vue";

export default {
  name: "login",
  components: {
    IconFont,
    DesktopIcon,
    LockOnIcon,
  },
  data() {
    return {
      formData: {
        account: "",
        password: "",
      },
      allCirle: [
        { class: "left_cir", ani: "left_animate" },
        { class: "left_top_cir", ani: "left_top_animate" },
        { class: "center_bot_cir", ani: "center_animate" },
        { class: "right_cir", ani: "right_animate" },
        { class: "right_top_cir", ani: "right_top_animate" },
      ],
      rules: {
        account: [{ required: true, message: "账号必填", type: "error" }],
        password: [
          { required: true, message: "密码必填", type: "error" },
          { min: 6, message: "请输入 6 位以上密码", type: "warning" },
          {
            pattern: /[A-Z]+/,
            message: "密码必须包含大写字母",
            type: "warning",
          },
        ],
      },
      loading: false,
      formdisabled: false,
    };
  },
  created() {
    sessionStorage.clear()
  },
  methods: {
    onSubmit({ validateResult, firstError }) {
      const that = this;
      that.loading = true;
      that.formdisabled = true;
      if (validateResult === true) {
        that.$http
          .post("/api/api/pwd/", {
            params: { 'account' : that.formData.account },
          })
          .then((response) => {
            if (response.data.errcode === 0) {
              if (response.data.data.password === "error") {
                this.$message.error("该用户不存在");
                that.loading = false;
                that.formdisabled = false;
              } else {
                if (response.data.data.password === that.formData.password) {
                  sessionStorage.setItem("username", this.formData.account);
                  this.$message.success("登录成功");
                  that.loading = false;
                  that.formdisabled = false;
                  this.$router.push("/index");
                } else {
                  this.$message.error("密码错误,请重试");
                  that.loading = false;
                  that.formdisabled = false;
                }
              }
            } else {
              that.$message.error("登陆失败");
              that.loading = false;
              that.formdisabled = false;
            }
          })
          .catch((error) => {
            console.log(error);
            that.$message.error("登陆失败");
            that.loading = false;
            that.formdisabled = false;
          });
      } else {
        console.log("Errors: ", validateResult);
        this.$message.warning(firstError);
        that.loading = false;
        that.formdisabled = false;
      }
    },
    OnUserIn() {
      this.$router.push("/index");
    },
  },
};
</script>
<style scoped>
.bg_circle {
  position: absolute;
  background-color: #f8f9fc;
  transition-duration: 3s;
}
.left_cir {
  top: 46px;
  left: -200px;
  width: 409px;
  height: 409px;
  background: linear-gradient(269deg, #f7f9ff 1%, #e5f0fe 99%);
  border-radius: 50%;
}
.left_top_cir {
  top: -142px;
  left: 274px;
  width: 225px;
  height: 225px;
  background: linear-gradient(90deg, #f7f9ff 1%, #e5f0fe 99%);
  border-radius: 50%;
}
.center_bot_cir {
  top: 300px;
  left: 274px;
  width: 269px;
  height: 269px;
  background: linear-gradient(269deg, #f7f9ff 1%, #e5f0fe 99%);
  border-radius: 50%;
}
.right_cir {
  top: 250px;
  right: 0px;
  opacity: 0.61;
  width: 429px;
  height: 429px;
  background: linear-gradient(269deg, #f7f9ff 1%, #e5f0fe 99%);
  border-radius: 50%;
}
.right_top_cir {
  top: -77px;
  right: 177px;
  opacity: 0.7;
  width: 144px;
  height: 144px;
  background: linear-gradient(269deg, #f7f9ff 1%, #e5f0fe 99%);
  border-radius: 50%;
}
.left_animate {
  transform: translateX(100px);
}
.left_top_animate {
  transform: translateY(100px);
}
.center_animate {
  transform: translateY(-100px);
}
.right_animate {
  transform: translateX(-100px);
}
.right_top_animate {
  transform: translateY(100px);
}
.login-box {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.login-container {
  padding: 20px;
  width: 400px;
  background: #ffffff;
  border-radius: 5px;
  box-shadow: 3px 3px 10px gray;
}
.login-title {
  left: 50%;
  transform: translate(-50%, 0%);
}
.submit-button {
  left: 50%;
  transform: translate(-50%, 0%);
}
</style>
