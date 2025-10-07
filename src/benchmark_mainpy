import time
import psutil
import os
import threading
from article_poster import ArticlePoster
from discord import send_discord_log
from config import config

class ResourceMonitor:
    def __init__(self):
        self.max_memory = 0
        self.avg_cpu = 0
        self.samples = 0
        self.stop_monitor = False
        self.process = psutil.Process(os.getpid())
        
    def monitor_loop(self):
        cpu_sum = 0
        sample_count = 0
        
        while not self.stop_monitor:
            try:
                # メモリ監視
                current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
                self.max_memory = max(self.max_memory, current_memory)
                
                # CPU監視
                cpu_usage = psutil.cpu_percent(interval=0.5)
                cpu_sum += cpu_usage
                sample_count += 1
                
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ モニタリングエラー: {e}")
                break
        
        self.avg_cpu = cpu_sum / sample_count if sample_count > 0 else 0
        self.samples = sample_count
    
    def start(self):
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop(self):
        self.stop_monitor = True
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)

def detailed_monitor(func):
    def wrapper(*args, **kwargs):
        monitor = ResourceMonitor()
        
        # システム全体の情報も取得
        system_memory_start = psutil.virtual_memory()
        system_cpu_start = psutil.cpu_percent(interval=None)
        
        print(f"🔍 リソース監視開始...")
        monitor.start()
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = None
            print(f"❌ 関数実行エラー: {e}")
        finally:
            end_time = time.time()
            monitor.stop()
        
        # システム全体の情報（終了時）
        system_memory_end = psutil.virtual_memory()
        system_cpu_end = psutil.cpu_percent(interval=1)
        
        execution_time = end_time - start_time
        
        print(f"\n📊 === 詳細リソースレポート ===")
        print(f"⏱️  総実行時間: {execution_time:.2f}秒")
        print(f"💾 最大メモリ使用量: {monitor.max_memory:.2f}MB")
        print(f"🖥️  平均CPU使用率: {monitor.avg_cpu:.2f}%")
        print(f"📈 監視サンプル数: {monitor.samples}回")
        
        # システム全体の情報
        print(f"💽 システムメモリ使用率: {system_memory_end.percent}%")
        print(f"🔧 システムCPU使用率: {system_cpu_end}%")
        print(f"📋 利用可能メモリ: {system_memory_end.available / 1024 / 1024:.0f}MB")
        
        # 推奨スペックの目安
        print(f"\n💡 推奨スペック目安:")
        print(f"  最小メモリ: {monitor.max_memory * 1.5:.0f}MB")
        print(f"  推奨メモリ: {monitor.max_memory * 2:.0f}MB")
        print(f"  CPUコア数: 1コア以上 (使用率 {monitor.avg_cpu:.1f}%)")
        
        return result
    return wrapper

@detailed_monitor
def main_job():
    """メインのジョブ実行"""
    print(f"🕒 ジョブ実行開始: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        poster = ArticlePoster(config.LIVEDOOR_USER_ID, config.LIVEDOOR_USER_PASSWD)
        result = poster.run()
        
        if result['status'] == 'success':
            print(f"✅ 投稿成功: {result.get('title', '')}")
            return result
        else:
            print(f"⚠️ 投稿失敗: {result.get('message', '')}")
            return result
            
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        raise  # エラーを再発生させてモニタリングで検知できるようにする

def monitor_system_resources():
    """システムリソースの監視"""
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage('/')
    
    print(f"📈 システム状態 - CPU: {cpu}% | メモリ: {memory.percent}% | ディスク: {disk.percent}%")
    
    # リソース使用率が高い場合に警告
    if memory.percent > 85:
        print("⚠️  警告: メモリ使用率が高いです")
    if cpu > 80:
        print("⚠️  警告: CPU使用率が高いです")

if __name__ == "__main__":
    print("🚀 一度きりのジョブ実行を開始します...")
    send_discord_log("🚀 一度きりのジョブ実行を開始します...")
    
    # システムリソースの初期状態を表示
    print("\n📊 システム初期状態:")
    monitor_system_resources()
    
    print("\n" + "="*50)
    
    # メインジョブの実行
    start_time = time.time()
    try:
        result = main_job()
        end_time = time.time()
        
        print("\n" + "="*50)
        print(f"🎉 ジョブ完了: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  総所要時間: {end_time - start_time:.2f}秒")
        
        # 結果に基づいたメッセージをDiscordに送信
        if result and result.get('status') == 'success':
            send_discord_log(f"✅ 投稿成功: {result.get('title', '')}")
        else:
            error_msg = result.get('message', '不明なエラー') if result else '実行エラー'
            send_discord_log(f"❌ 投稿失敗: {error_msg}")
            
    except Exception as e:
        end_time = time.time()
        print(f"\n💥 ジョブ異常終了: {e}")
        print(f"⏱️  実行時間: {end_time - start_time:.2f}秒")
        send_discord_log(f"💥 ジョブ異常終了: {e}")
    
    print("👋 プログラムを終了します")
