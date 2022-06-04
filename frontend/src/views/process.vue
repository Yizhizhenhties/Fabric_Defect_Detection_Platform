<template>
  <div class="process">
    <t-row style="height: 4%">
      <div>
        <img
          slot="clothe"
          class="clothe"
          src="../assets/clothe.png"
          alt="clohte"
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
        纺织物缺陷检测
      </span>
    </t-row>
    <t-row style="height: 5%" />
    <t-row style="height: 8%">
      <span style="font-family: fangsong; font-size: 18px; margin-left: 30px">
        请点击左边选择框中的按钮选择图片(最多九张),点击传输按钮等待上传处理即可
      </span>
    </t-row>
    <t-row style="height: 3%" />
    <t-row style="height: 80%">
      <t-col
        :span="10"
        style="
          border: dashed;
          height: 100%;
          border-radius: 12px;
          border-color: steelblue;
        "
      >
        <div class="upLoad">
          <div class="title">
            <div class="shuju">
              <span
                >当前张数：{{ this.imgList.length }} /
                {{ this.maxNumber }} 张</span
              >
              <span>当前大小：{{ this.bySize }}</span>
            </div>
          </div>
          <div
            class="photobox"
            @drop="drop($event)"
            @dragenter="dragenter($event)"
            @dragover="dragover($event)"
          >
            <div
              class="photo-item"
              v-show="imgList.length > 0"
              v-for="(item, index) in imgList"
              :key="index"
            >
              <div class="pic-del">
                <icon
                  name="close"
                  class="iconfont icon-shanchu del"
                  @click="delImg(index)"
                ></icon>
              </div>
              <div class="pic-img">
                <img :src="item.file.src" alt="" />
              </div>
            </div>
            <div v-if="imgList.length < maxNumber" class="photo-item-btn">
              <input
                type="file"
                name="upimg"
                accept="image/*"
                class="fileimg"
                ref="updateimg"
                @change="updateImg($event)"
                multiple
              />
              <i class="iconfont icon-tianjia"></i>
              <span>点击添加或拖拽图片</span>
            </div>
          </div>
        </div>
      </t-col>
      <t-col :span="2" style="height: 100%">
        <t-button
          class="process-button"
          theme="primary"
          shape="circle"
          @click="showValidate"
        >
          <icon-font name="arrow-right" />
        </t-button>
      </t-col>
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
        <t-button
          theme="default"
          style="margin-right: 5px"
          :disabled="pass_disabled"
          @click="PassValidate"
          >跳过</t-button
        >
        <t-button
          style="margin-right: 5px"
          :disabled="commit_disabled"
          @click="GoValidate"
          >提交</t-button
        >
      </div>
    </t-dialog>
  </div>
</template>

<script>
import { AddIcon, IconFont, Icon } from "tdesign-icons-vue";
import axios from "axios";
export default {
  name: "process",
  components: { AddIcon, IconFont, Icon },
  data() {
    return {
      //上传数量上限
      maxNumber: 9,
      //上传文件列表
      imgList: [],
      //格式过滤列表
      filterList: ["image/gif", "image/jpeg", "image/png", "image/x-icon"],
      //文件总大小
      size: 0,
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
      imgs: [
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
        { src: require("../assets/blank.png") },
      ],
      pass_disabled: false,
      commit_disabled: false,
      right: null,
    };
  },
  methods: {
    //拖拽三连
    dragenter(el) {
      el.stopPropagation();
      el.preventDefault();
    },
    dragover(el) {
      el.stopPropagation();
      el.preventDefault();
    },
    drop(el) {
      el.stopPropagation();
      el.preventDefault();
      if (this.imgList.length + el.dataTransfer.files.length > this.maxNumber) {
        this.$message.error("已经超出张数！");
        return;
      } else {
        //拖拽的文件上传
        this.filesList(el.dataTransfer.files);
      }
    },
    //遍历图片列表
    filesList(files) {
      [...files]
        .filter((v) => this.filterList.indexOf(v.type) !== -1)
        .forEach((v) => this.fileAdd(v));
    },
    //添加到渲染列表
    fileAdd(file) {
      this.size += file.size; //总大小
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        file.src = reader.result;
        this.imgList.push({ file });
      };
    },
    //input选择文件上传
    updateImg(el) {
      if (this.imgList.length + el.target.files.length > this.maxNumber) {
        this.$message.error("已经超出张数！");
        return;
      } else {
        //拖拽的文件上传
        this.filesList(el.target.files);
      }
    },
    //删除图片
    delImg(index) {
      this.size -= this.imgList[index].file.size; //总大小
      this.imgList.splice(index, 1);
    },
    GoToOutput() {
      this.$router.push({
        name: "output",
        params: {
          data: this.imgList,
        },
      });
    },
    showValidate() {
      if (this.imgList.length < 1) {
        this.$message.error("请至少选择一张图片");
        return;
      }
      if(sessionStorage.getItem("validatecookie") === "true"){
        this.GoToOutput()
      }
      this.validate_visible = true;
      this.validate_loading = true;
      this.commit_disabled = true;
      this.right = null;
      for (var i = 0; i < this.selectedList.length; i++) {
        this.selectedList[i] = false;
      }
      for (var i = 0; i < this.imgs.length; i++) {
        this.$refs.va_img[i].style.filter = "";
        this.$refs.mengceng[i].style.display = "none";
      }
      this.$http
        .post("/api/api/validate/", {
          params: {},
        })
        .then((response) => {
          if (response.data.errcode === 0) {
            this.right = response.data.right;
            for (let i = 0; i < 9; i++) {
              this.imgs[i].src = response.data.data[i].va_img;
            }
            this.validate_loading = false;
            this.commit_disabled = false;
          } else {
            this.$message.error("获取验证码失败");
            this.validate_loading = false;
          }
        })
        .catch((error) => {
          this.$message.error("获取验证码失败");
          this.validate_loading = false;
        });
    },
    PassValidate() {
      this.validate_loading = true;
      this.commit_disabled = true;
      this.right = null;
      for (var i = 0; i < this.selectedList.length; i++) {
        this.selectedList[i] = false;
      }
      for (var i = 0; i < this.imgs.length; i++) {
        this.$refs.va_img[i].style.filter = "";
        this.$refs.mengceng[i].style.display = "none";
      }
      this.$http
        .post("/api/api/validate/", {
          params: {},
        })
        .then((response) => {
          if (response.data.errcode === 0) {
            this.right = response.data.right;
            for (let i = 0; i < 9; i++) {
              this.imgs[i].src = response.data.data[i].va_img;
            }
            this.validate_loading = false;
            this.commit_disabled = false;
          } else {
            this.$message.error("获取验证码失败");
            this.validate_loading = false;
          }
        })
        .catch((error) => {
          this.$message.error("获取验证码失败");
          this.validate_loading = false;
        });
    },
    GoValidate() {
      if (this.right === "-2") {
        this.validate_visible = false;
        this.GoToOutput();
      }
      this.validate_loading = true;
      this.commit_disabled = true;
      this.pass_disabled = true;
      let check = [];
      for (var i = 0; i < this.selectedList.length; i++) {
        if (this.selectedList[i]) {
          check.push(i + 1 + "");
        }
      }
      if (check.length === 0) {
        check.push("-1");
      }
      let check_str = check.join("");
      if (check_str === this.right) {
        this.validate_loading = false;
        this.commit_disabled = false;
        this.pass_disabled = false;
        this.validate_visible = false;
        this.$message.success("验证成功");
        sessionStorage.setItem("validatecookie", "true");
        this.GoToOutput();
      } else {
        this.$message.error("验证失败，请重新选择");
        this.validate_loading = false;
        this.commit_disabled = false;
        this.pass_disabled = false;
      }
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
  computed: {
    //计算大小
    bySize() {
      if (this.size === 0) return "0 B";
      let k = 1024,
        sizes = ["B", "KB", "MB", "GB"],
        i = Math.floor(Math.log(this.size) / Math.log(k));
      return (this.size / Math.pow(k, i)).toPrecision(3) + " " + sizes[i];
    },
  },
};
</script>

<style>
.process {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
.process-button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.generation {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.tdesign-demo-upload-item {
  display: inline-block;
  margin-right: 80px;
}
.tdesign-demo-upload-item + .tdesign-demo-upload-item {
  margin-top: 80px;
}
.upLoad {
  position: relative;
}
.upimg {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  margin: auto;
  overflow: hidden;
  width: 1200px;
  min-height: 500px;
  height: 700px;
  font-size: 12px;
  border-radius: 5px;
  box-shadow: 0 0 5px #535658;
}
.title {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  font-size: 16px;
  color: #666;
}
.title .shuju {
  flex: 1;
}
.title .shuju span {
  margin-right: 20px;
}
.photobox {
  overflow: hidden;
  padding: 10px 6px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
.photo-item {
  position: relative;
  float: left;
  margin: 0 10px 6px;
  width: 160px;
  height: 160px;
  text-align: center;
  border: 1px solid #e1e1e1;
}
.photo-item:hover .pic-del {
  display: block;
}
.photo-item .pic-del {
  display: none;
  position: absolute;
  bottom: 40px;
  left: 0;
  padding-right: 6px;
  width: 100%;
  height: 30px;
  background-color: rgba(0, 0, 0, 0.3);
  box-sizing: border-box;
}
.photo-item .pic-del .del {
  float: right;
  color: #fff;
  font-size: 26px;
  cursor: pointer;
}
.photo-item .pic-img {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 158px;
}
.photo-item .pic-img img {
  max-width: 100%;
  max-height: 100%;
  vertical-align: middle;
}
.photo-item-btn {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  float: left;
  margin: 0 15px 10px;
  width: 160px;
  height: 160px;
  border: 1px dashed #e1e1e1;
  border-radius: 6px;
  font-size: 16px;
  color: #ccc;
}
.photo-item-btn i {
  font-size: 40px;
  margin-bottom: 20px;
}
.photo-item-btn .fileimg {
  position: absolute;
  top: 0;
  left: 0;
  width: 160px;
  height: 160px;
  opacity: 0;
  cursor: pointer;
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