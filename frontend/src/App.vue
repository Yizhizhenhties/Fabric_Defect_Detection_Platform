<template>
  <div class="tdesign-demo-item--layout">
    <transition name="transitionRouter">
      <router-view></router-view>
    </transition>
  </div>
</template>
<script>
export default {
  data() {
    return {};
  },
};
</script>
<style>
.transitionRouter-enter-active {
  transition: all 0.7s ease;
}
.transitionRouter-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.6, 0.6, 1);
}

.transitionRouter-enter,
.transitionRouter-leave {
  opacity: 0;
}
</style>