const OSS = require('ali-oss');
const fs = require('fs');
const path = require('path');

const client = new OSS({
  region: 'oss-cn-beijing',
  accessKeyId: 'YOUR_ACCESS_KEY_ID',
  accessKeySecret: 'YOUR_ACCESS_KEY_SECRET',
  bucket: 'beijingyuyan'
});

async function uploadFile(localPath, ossPath) {
  try {
    const result = await client.put(ossPath, localPath);
    console.log(`✅ 上传成功: ${ossPath}`);
    console.log(`   URL: ${result.url}`);
    return result.url;
  } catch (error) {
    console.error(`❌ 上传失败: ${ossPath}`, error.message);
    throw error;
  }
}

async function main() {
  console.log('🚀 开始上传数据到OSS...\n');
  
  try {
    // 上传景点数据
    const attractionsUrl = await uploadFile(
      '/Users/jiyi/.openclaw/workspace/data/attractions.json',
      'data/attractions.json'
    );
    
    // 上传路线数据
    const routesUrl = await uploadFile(
      '/Users/jiyi/.openclaw/workspace/data/routes.json',
      'data/routes.json'
    );
    
    console.log('\n🎉 所有数据上传完成!');
    console.log('\n📊 数据访问地址:');
    console.log(`   景点数据: https://beijingyuyan.oss-cn-beijing.aliyuncs.com/data/attractions.json`);
    console.log(`   路线数据: https://beijingyuyan.oss-cn-beijing.aliyuncs.com/data/routes.json`);
    
  } catch (error) {
    console.error('\n❌ 上传过程出错:', error.message);
    process.exit(1);
  }
}

main();
