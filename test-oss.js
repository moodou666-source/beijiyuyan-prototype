const OSS = require('ali-oss');

const client = new OSS({
  region: 'oss-cn-beijing',
  accessKeyId: 'YOUR_ACCESS_KEY_ID',
  accessKeySecret: 'YOUR_ACCESS_KEY_SECRET',
  bucket: 'beijingyuyan'
});

async function testConnection() {
  try {
    // 测试连接 - 列出Bucket中的文件
    const result = await client.list({
      'max-keys': 10
    });
    console.log('✅ OSS连接成功!');
    console.log('📦 Bucket名称:', 'beijingyuyan');
    console.log('📁 当前文件数:', result.objects ? result.objects.length : 0);
    if (result.objects && result.objects.length > 0) {
      console.log('\n📄 现有文件列表:');
      result.objects.forEach((obj, i) => {
        console.log(`  ${i+1}. ${obj.name}`);
      });
    }
    return true;
  } catch (error) {
    console.error('❌ OSS连接失败:', error.message);
    return false;
  }
}

testConnection();
