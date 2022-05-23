<template>
  <div class="index">
    <t-layout>
      <t-header style="height: 8vh">
        <t-head-menu value="item1">
          <img
            slot="logo"
            width="240"
            class="logo"
            src="../assets/logo.png"
            alt="logo"
            style="margin-left: 40px"
          />
          <template #operations>
            <t-tooltip placement="bottom" content="回到首页">
              <t-button
                theme="default"
                shape="square"
                variant="text"
                size="large"
                style="margin-right: 8px"
                @click="goToHome"
              >
                <t-icon name="home" />
              </t-button>
            </t-tooltip>
            <t-tooltip placement="bottom" content="帮助文档">
              <t-button
                theme="default"
                shape="square"
                variant="text"
                size="large"
                style="margin-right: 8px"
                @click="goToHelper"
              >
                <t-icon name="help-circle" />
              </t-button>
            </t-tooltip>
            <t-tooltip placement="bottom" content="代码仓库">
              <t-button
                theme="default"
                shape="square"
                variant="text"
                size="large"
                style="margin-right: 8px"
                @click="goToGithub"
              >
                <t-icon name="logo-github" />
              </t-button>
            </t-tooltip>
            <t-dropdown
              :min-column-width="125"
              trigger="click"
              style="margin-right: 20px"
            >
              <template #dropdown>
                <t-dropdown-menu>
                  <t-dropdown-item
                    class="operations-dropdown-container-item"
                    @click="goToRecord"
                  >
                    <t-icon name="time" size="large"></t-icon>历史记录
                  </t-dropdown-item>
                  <t-dropdown-item
                    class="operations-dropdown-container-item"
                    @click="modalvisible = true"
                  >
                    <t-icon name="poweroff" size="large"></t-icon>退出登录
                  </t-dropdown-item>
                </t-dropdown-menu>
              </template>
              <t-button class="header-user-btn" theme="default" variant="text">
                <template #icon>
                  <t-icon
                    class="header-user-avatar"
                    name="user-circle"
                    size="large"
                  />
                </template>
                <div class="header-user-account">
                  {{ username }}
                  <t-icon name="chevron-down" />
                </div>
              </t-button>
            </t-dropdown>
          </template>
        </t-head-menu>
      </t-header>
      <t-content
        style="
          padding-left: 20px;
          padding-right: 20px;
          padding-top: 20px;
          height: 84vh;
        "
      >
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </t-content>
      <t-footer style="align-self: center; height: 8vh">
        <div class="about-us">
          <a
            :style="avtivecolor"
            @mouseover="Mouseover()"
            @mouseleave="Mouseleave()"
            @click="goToAboutUs"
          >
            关于我们
          </a>
          <t-divider layout="vertical" />
          <a
            :style="avtivecolor1"
            @mouseover="Mouseover1()"
            @mouseleave="Mouseleave1()"
            @click="goToContactUs"
          >
            联系我们
          </a>
        </div>
      </t-footer>
    </t-layout>
    <t-dialog
      :visible.sync="modalvisible"
      theme="info"
      header="提示"
      body="是否确定退出登录"
      @confirm="onConfirm"
    >
    </t-dialog>
  </div>
</template>

<script>
import { UserIcon } from "tdesign-icons-vue";

export default {
  name: "index",
  components: { UserIcon },
  data() {
    return {
      allCirle: [
        { class: "left_cir", ani: "left_animate" },
        { class: "left_top_cir", ani: "left_top_animate" },
        { class: "center_bot_cir", ani: "center_animate" },
        { class: "right_cir", ani: "right_animate" },
        { class: "right_top_cir", ani: "right_top_animate" },
      ],
      username: "",
      avtivecolor: "color: black",
      avtivecolor1: "color: black",
      modalvisible: false,
    };
  },
  methods: {
    onConfirm() {
      this.modalvisible = false;
      sessionStorage.clear()
      this.$router.push('/')
    },
    getUserInfo() {
      const that = this;
      if (sessionStorage.getItem("username")) {
        that.username = sessionStorage.getItem("username");
      } else {
        that.username = "游客";
      }
    },
    goToRecord() {
      const that = this;
      that.$router.push("history");
    },
    goToHome() {
      const that = this;
      that.$router.push("process");
    },
    goToGithub() {
      const that = this;
      window.open(
        "https://github.com/Yizhizhenhties/Fabric_Defect_Detection_Platform"
      );
    },
    goToAboutUs() {
      const that = this;
      that.$router.push("aboutus");
    },
    goToContactUs() {
      const that = this;
      that.$router.push("contactus");
    },
    goToHelper() {
      const that = this;
      that.$router.push("helper");
    },
    Mouseover() {
      this.avtivecolor = "color: #2e81f9"; // 进入 悬停区域,更改文字颜色
    },
    Mouseleave() {
      this.avtivecolor = "color:black"; // 离开 悬停区域,文字颜色复原
    },
    Mouseover1() {
      this.avtivecolor1 = "color: #2e81f9"; // 进入 悬停区域,更改文字颜色
    },
    Mouseleave1() {
      this.avtivecolor1 = "color:black"; // 离开 悬停区域,文字颜色复原
    },
  },
  created() {
    const that = this;
    this.getUserInfo();
  },
};
</script>
<style lang="less">
.fade-leave-active,
.fade-enter-active {
  transition: opacity 0.28s cubic-bezier(0.38, 0, 0.24, 1);
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.operations-dropdown-container-item {
  width: 100%;
  display: flex;
  align-items: center;

  .t-icon {
    margin-right: 8px;
  }

  .t-dropdown__item {
    .t-dropdown__item__content {
      display: flex;
      justify-content: center;
    }
    .t-dropdown__item__content__text {
      display: flex;
      align-items: center;
      font-size: 14px;
    }
  }

  .t-dropdown__item {
    width: 100%;
    margin-bottom: 0px;
  }
  &:last-child {
    .t-dropdown__item {
      margin-bottom: 8px;
    }
  }
}
</style>
