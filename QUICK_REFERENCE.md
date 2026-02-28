# 設計模式快速參考卡

## 🎯 四大設計模式快速查找

### 1️⃣ 策略模式 (Strategy)
**檔案**: `attack_strategy.py`

**何時使用**: 需要多種算法/行為

**快速用法**:
```python
# 創建塔
tower = Tower(100, 100, 'basic')

# 改變攻擊策略
tower.set_attack_strategy(StrongestEnemyStrategy())

# 使用其他策略
tower.set_attack_strategy(FastestEnemyStrategy())
tower.set_attack_strategy(FarthestEnemyStrategy())
```

**可用策略**:
- `ClosestEnemyStrategy()` - 最近敵人
- `FastestEnemyStrategy()` - 最快敵人
- `StrongestEnemyStrategy()` - 最強敵人
- `FarthestEnemyStrategy()` - 最先進敵人

---

### 2️⃣ 狀態模式 (State)
**檔案**: `tower_state.py`

**何時使用**: 對象有多個狀態，行為不同

**快速用法**:
```python
from tower_state import AttackingState, IdleState, UpgradedState

tower = Tower(100, 100, 'basic')

# 改變狀態
tower.set_state(AttackingState())
tower.set_state(IdleState())

# 升級後自動轉換
tower.upgrade()  # 自動變為 UpgradedState

# 查詢當前狀態
print(tower.state.get_state_name())
```

**可用狀態**:
- `IdleState()` - 閒置
- `AttackingState()` - 攻擊
- `UpgradedState()` - 升級
- `CooldownState(frames)` - 冷卻

---

### 3️⃣ 觀察者模式 (Observer)
**檔案**: `event_system.py`

**何時使用**: 對象間需要解耦通信

**快速用法**:
```python
from event_system import EventManager, GameEvent

# 獲取事件管理器
events = EventManager()

# 訂閱事件 (方式1: 回調)
def on_kill(event, data):
    print(f"敵人被擊殺! 獎勵: {data['reward']}")

events.subscribe_callback(GameEvent.ENEMY_KILLED, on_kill)

# 發射事件
events.emit(GameEvent.ENEMY_KILLED, {'reward': 10})
```

**主要事件**:
- `TOWER_PLACED` - 塔被放置
- `TOWER_UPGRADED` - 塔被升級
- `ENEMY_KILLED` - 敵人被殺
- `ENEMY_ESCAPED` - 敵人逃脫
- `MONEY_CHANGED` - 金錢變化
- `LIVES_CHANGED` - 生命值變化
- `WAVE_STARTED` - 波次開始
- `WAVE_COMPLETED` - 波次完成

---

### 4️⃣ 建造者模式 (Builder)
**檔案**: `tower_builder.py`

**何時使用**: 創建複雜對象配置

**快速用法**:
```python
from tower_builder import TowerBuilder, TowerConfiguration

# 方式1: 使用流式API
tower = (TowerBuilder('basic')
    .at_position(100, 100)
    .with_level(2)
    .with_damage(50)
    .build())

# 方式2: 使用預定義配置
tower = TowerConfiguration.sniper_tower(200, 200)
tower = TowerConfiguration.cannon_tower(300, 300)

# 方式3: 完全自定義
tower = (TowerBuilder('cannon')
    .at_position(150, 150)
    .with_level(3)
    .with_damage(80)
    .with_range(200)
    .with_aoe(60)
    .build())

# 升級構造器
from tower_builder import TowerUpgradeBuilder
upgrade = TowerUpgradeBuilder(tower)
upgrade.upgrade_levels(1).add_damage_bonus(20).apply()
```

---

## 📖 常見操作

### 添加新的攻擊策略
1. 在 `attack_strategy.py` 中創建新類
2. 繼承 `AttackStrategy`
3. 實現 `get_target()` 和 `attack()` 方法
4. 使用 `tower.set_attack_strategy()`

### 添加新的塔狀態
1. 在 `tower_state.py` 中創建新類
2. 繼承 `TowerState`
3. 實現必要的方法
4. 使用 `tower.set_state()`

### 添加新的遊戲事件
1. 在 `event_system.py` 的 `GameEvent` 中添加
2. 在適當的地方調用 `event_manager.emit()`
3. 訂閱並處理事件

### 添加新的塔配置
1. 在 `tower_builder.py` 的 `TowerConfiguration` 中添加方法
2. 使用 `TowerBuilder` 配置
3. 提供快速訪問方法

---

## 🔗 集成矩陣

| 模式 | 集成於 | 用途 |
|------|--------|------|
| 策略 | tower.py | 選擇攻擊目標 |
| 狀態 | tower.py | 管理塔的狀態 |
| 觀察者 | game.py, enemy.py | 事件通知 |
| 建造者 | game.py | 創建塔 |

---

## 📊 模式選擇流程圖

```
需要添加功能?
│
├─ 多種算法/行為? 
│  └─> 使用 策略模式 (Strategy)
│
├─ 狀態管理?
│  └─> 使用 狀態模式 (State)
│
├─ 對象通信?
│  └─> 使用 觀察者模式 (Observer)
│
└─ 複雜配置?
   └─> 使用 建造者模式 (Builder)
```

---

## 🎓 學習路徑

### 初級
1. 了解四個基本模式
2. 查看 `design_patterns_demo.py`
3. 運行驗證腳本

### 中級
1. 根據指南添加新策略
2. 實現新事件
3. 創建自定義塔配置

### 高級
1. 組合多個模式
2. 優化性能
3. 添加新的設計模式

---

## 🐛 調試技巧

### 查看當前塔狀態
```python
print(tower.state.get_state_name())
```

### 查看當前策略
```python
print(type(tower.attack_strategy).__name__)
```

### 監控事件
```python
from event_system import GameEventObserver
observer = GameEventObserver("Debug")
game.event_manager.subscribe(GameEvent.TOWER_PLACED, observer)
```

### 驗證配置
```python
python3 validate_patterns.py
```

---

## 📚 詳細資源

- **完整文檔**: [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md)
- **使用指南**: [REFACTORING_GUIDE.md](REFACTORING_GUIDE.md)
- **重構報告**: [REFACTORING_REPORT.md](REFACTORING_REPORT.md)
- **代碼示例**: [design_patterns_demo.py](design_patterns_demo.py)

---

## ✅ 快速檢查清單

- [ ] 了解策略模式
- [ ] 了解狀態模式
- [ ] 了解觀察者模式
- [ ] 了解建造者模式
- [ ] 運行驗證腳本
- [ ] 查看演示代碼
- [ ] 試著添加新策略
- [ ] 試著訂閱事件
- [ ] 試著使用構造器

---

**最後更新**: 2026年2月28日  
**快速參考版本**: 1.0
