<template>
  <div class="history">
    <t-row style="height: 4%">
      <div>
        <img
          slot="history_img"
          class="history_img"
          src="../assets/history.png"
          alt="history_img"
          style="margin-left: 40px; width: 24px"
        />
      </div>
      <span
        style="
          font-family: cursive;
          font-size: 24px;
          font-weight: bold;
          margin-left: 10px;
        "
      >
        历史记录
      </span>
    </t-row>
    <t-row style="height: 5%" />
    <t-row>
      <input
        type="file"
        name="upimg"
        accept="image/*"
        class="fileimg"
        ref="updateimg"
        @change="updateImg($event)"
        multiple
      />
      <t-button @click="upload">确定上传</t-button>
      <span>预测结果: {{ predict }}</span>
    </t-row>
    <t-row>
      <t-button @click="showValidate">展示</t-button>
    </t-row>
    <t-dialog
      :visible.sync="validate_visible"
      :footer="false"
      :header="false"
      :closeBtn="null"
      placement="center"
    >
      <div style="margin-left: 5px">
        <h2 style="color: black">请选择图中纺织品缺陷部分</h2>
      </div>
      <t-loading :loading="validate_loading">
        <div class="covers">
          <div class="cover" v-for="(img, index) in imgs" :key="index">
            <img
              ref="va_img"
              :src="img.src"
              alt=""
              @click="ChangeValidateList(index)"
              class="validateimg"
            />
            <span
              ref="mengceng"
              class="mengceng"
              style="display: none"
              @click="ChangeValidateList(index)"
              >√</span
            >
          </div>
        </div>
      </t-loading>
      <div style="margin-top: 20px; float: right">
        <t-button theme="default" style="margin-right: 5px" :disabled="pass_disabled" @click="PassValidate">跳过</t-button>
        <t-button style="margin-right: 5px" :disabled="commit_disabled" @click="GoValidate">提交</t-button>
      </div>
    </t-dialog>
  </div>
</template>

<script>
export default {
  name: "history",
  components: {},
  data() {
    return {
      selectedList: [
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
      ],
      validate_visible: false,
      validate_loading: false,
      maxNumber: 9,
      predict: null,
      imgList: [],
      filterList: ["image/gif", "image/jpeg", "image/png", "image/x-icon"],
      imgs: [
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_2.png") },
        { src: require("../assets/5_1.png") },
      ],
      pass_disabled: false,
      commit_disabled: false
    };
  },
  methods: {
    filesList(files) {
      [...files]
        .filter((v) => this.filterList.indexOf(v.type) !== -1)
        .forEach((v) => this.fileAdd(v));
    },
    fileAdd(file) {
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        file.src = reader.result;
        this.imgList.push({ file });
      };
    },
    updateImg(el) {
      this.filesList(el.target.files);
    },
    upload() {
      var imgfilelist = new FormData();
      this.imgList.forEach((value, index) => {
        imgfilelist.append("file", value.file);
      });
      this.$http
        .post("/api/api/ex4/", imgfilelist, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response) => {
          if (response.data.errcode === 0) {
            for (let i = 0; i < response.data.data.length; i++) {
              this.predict = response.data.data[i].output;
            }
          } else {
            this.$message.error("服务器连接失败");
          }
        })
        .catch((error) => {
          this.$message.error("服务器连接失败");
        });
    },
    showValidate() {
      this.validate_visible = true;
      this.validate_loading = true;
      this.commit_disabled = true;
      for (var i = 0; i < this.imgs.length; i++) {
        this.$refs.va_img[i].style.filter = "";
        this.$refs.mengceng[i].style.display = "none";
      }
      /*请求*/
      this.validate_loading = false;
      this.commit_disabled = false;
    },
    PassValidate() {
      this.validate_loading = true;
      this.commit_disabled = true;
      for (var i = 0; i < this.imgs.length; i++) {
        this.$refs.va_img[i].style.filter = "";
        this.$refs.mengceng[i].style.display = "none";
      }
      /*请求*/
      this.validate_loading = false;
      this.commit_disabled = false;
    },
    GoValidate(){
      this.validate_loading = true;
      this.commit_disabled = true;
      this.pass_disabled = true;
      let check = []
      for (var i = 0; i < this.selectedList.length; i++) {
        if(this.selectedList[i]){
          check.push(i)
        }
      }
      if(check.length === 0){
        check.push(-1)
      }
      /*请求*/
      console.log(check)
      this.validate_loading = false;
      this.commit_disabled = false;
      this.pass_disabled = false;
    },
    ChangeValidateList(index) {
      if (this.selectedList[index]) {
        this.selectedList[index] = false;
      } else {
        this.selectedList[index] = true;
      }
      for (var i = 0; i < this.imgs.length; i++) {
        if (i == index) {
          if (this.selectedList[index]) {
            this.$refs.va_img[i].style.filter = "opacity(0.7)";
            this.$refs.mengceng[i].style.display = "";
          } else {
            this.$refs.va_img[i].style.filter = "";
            this.$refs.mengceng[i].style.display = "none";
          }
        }
      }
    },
  },
};
</script>

<style>
.history {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
.covers {
  height: 400px;
  widows: 400px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}
.cover {
  display: flex;
  justify-content: center;
  width: 33%;
  padding: 3px;
  align-items: center;
}
.mengceng {
  font-weight: bold;
  position: absolute;
  font-size: 28px;
  color: rgb(45 91 166);
  cursor: pointer;
}
.validateimg {
  height: 95%;
  width: 95%;
  border-radius: 10px;
  cursor: pointer;
}
</style>