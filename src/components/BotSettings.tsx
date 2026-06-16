import { useState } from 'react'
import './BotSettings.css'

export interface BotConfig {
  id: string
  platform: 'telegram' | 'discord' | 'slack' | 'wechat'
  name: string
  enabled: boolean
  config: {
    botToken?: string
    chatId?: string
    webhookUrl?: string
    channelId?: string
    apiKey?: string
  }
  testStatus?: 'success' | 'failed' | 'testing'
  lastTested?: number
}

interface BotSettingsProps {
  onSave: (configs: BotConfig[]) => void
}

const platformInfo = {
  telegram: {
    icon: '📱',
    name: 'Telegram',
    fields: [
      { key: 'botToken', label: 'Bot Token', placeholder: '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz', type: 'password' },
      { key: 'chatId', label: 'Chat ID', placeholder: '123456789', type: 'text' }
    ],
    guide: 'https://core.telegram.org/bots#how-do-i-create-a-bot'
  },
  discord: {
    icon: '💬',
    name: 'Discord',
    fields: [
      { key: 'webhookUrl', label: 'Webhook URL', placeholder: 'https://discord.com/api/webhooks/...', type: 'password' }
    ],
    guide: 'https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks'
  },
  slack: {
    icon: '💼',
    name: 'Slack',
    fields: [
      { key: 'webhookUrl', label: 'Webhook URL', placeholder: 'https://hooks.slack.com/services/...', type: 'password' }
    ],
    guide: 'https://api.slack.com/messaging/webhooks'
  },
  wechat: {
    icon: '💚',
    name: '企业微信',
    fields: [
      { key: 'webhookUrl', label: 'Webhook URL', placeholder: 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...', type: 'password' }
    ],
    guide: 'https://developer.work.weixin.qq.com/document/path/91770'
  }
}

export function BotSettings({ onSave }: BotSettingsProps) {
  const [bots, setBots] = useState<BotConfig[]>([])
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingBot, setEditingBot] = useState<BotConfig | null>(null)
  const [selectedPlatform, setSelectedPlatform] = useState<keyof typeof platformInfo>('telegram')

  // 添加或编辑机器人
  const handleSaveBot = (bot: BotConfig) => {
    let updatedBots: BotConfig[]
    if (editingBot) {
      updatedBots = bots.map(b => b.id === bot.id ? bot : b)
    } else {
      updatedBots = [...bots, { ...bot, id: Date.now().toString() }]
    }
    setBots(updatedBots)
    onSave(updatedBots)
    setShowAddModal(false)
    setEditingBot(null)
  }

  // 删除机器人
  const handleDeleteBot = (id: string) => {
    if (confirm('确定要删除这个机器人配置吗？')) {
      const updatedBots = bots.filter(b => b.id !== id)
      setBots(updatedBots)
      onSave(updatedBots)
    }
  }

  // 切换启用状态
  const toggleBotEnabled = (id: string) => {
    const updatedBots = bots.map(b =>
      b.id === id ? { ...b, enabled: !b.enabled } : b
    )
    setBots(updatedBots)
    onSave(updatedBots)
  }

  // 测试机器人
  const testBot = async (bot: BotConfig) => {
    const updatedBots = bots.map(b =>
      b.id === bot.id ? { ...b, testStatus: 'testing' as const } : b
    )
    setBots(updatedBots)

    try {
      const response = await fetch('/api/bot/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bot)
      })

      const result = await response.json()
      const finalBots = bots.map(b =>
        b.id === bot.id ? {
          ...b,
          testStatus: result.success ? 'success' as const : 'failed' as const,
          lastTested: Date.now()
        } : b
      )
      setBots(finalBots)
      onSave(finalBots)
    } catch (error) {
      const finalBots = bots.map(b =>
        b.id === bot.id ? {
          ...b,
          testStatus: 'failed' as const,
          lastTested: Date.now()
        } : b
      )
      setBots(finalBots)
      onSave(finalBots)
    }
  }

  return (
    <div className="bot-settings">
      <div className="bot-settings-header">
        <h3>🤖 机器人通知</h3>
        <button
          className="btn-add-bot"
          onClick={() => {
            setEditingBot(null)
            setSelectedPlatform('telegram')
            setShowAddModal(true)
          }}
        >
          + 添加机器人
        </button>
      </div>

      <div className="bot-list">
        {bots.length > 0 ? (
          bots.map(bot => (
            <BotCard
              key={bot.id}
              bot={bot}
              onEdit={() => {
                setEditingBot(bot)
                setSelectedPlatform(bot.platform)
                setShowAddModal(true)
              }}
              onDelete={() => handleDeleteBot(bot.id)}
              onToggle={() => toggleBotEnabled(bot.id)}
              onTest={() => testBot(bot)}
            />
          ))
        ) : (
          <div className="no-bots">
            <p>暂未配置机器人</p>
            <p style={{ fontSize: '12px' }}>添加机器人后，预警将自动推送到社交平台</p>
          </div>
        )}
      </div>

      {showAddModal && (
        <BotConfigModal
          platform={selectedPlatform}
          editingBot={editingBot}
          onClose={() => {
            setShowAddModal(false)
            setEditingBot(null)
          }}
          onSave={handleSaveBot}
          onPlatformChange={setSelectedPlatform}
        />
      )}
    </div>
  )
}

// 机器人卡片组件
function BotCard({
  bot,
  onEdit,
  onDelete,
  onToggle,
  onTest
}: {
  bot: BotConfig
  onEdit: () => void
  onDelete: () => void
  onToggle: () => void
  onTest: () => void
}) {
  const platform = platformInfo[bot.platform]

  return (
    <div className={`bot-card ${bot.enabled ? 'enabled' : 'disabled'}`}>
      <div className="bot-card-header">
        <div className="bot-info">
          <span className="bot-icon">{platform.icon}</span>
          <div>
            <div className="bot-name">{bot.name}</div>
            <div className="bot-platform">{platform.name}</div>
          </div>
        </div>
        <div className="bot-status">
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={bot.enabled}
              onChange={onToggle}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>
      </div>

      <div className="bot-card-body">
        {bot.testStatus && (
          <div className={`test-status ${bot.testStatus}`}>
            {bot.testStatus === 'testing' && '⏳ 测试中...'}
            {bot.testStatus === 'success' && '✅ 测试成功'}
            {bot.testStatus === 'failed' && '❌ 测试失败'}
            {bot.lastTested && (
              <span className="test-time">
                {new Date(bot.lastTested).toLocaleTimeString()}
              </span>
            )}
          </div>
        )}
      </div>

      <div className="bot-card-actions">
        <button className="btn-icon-action" onClick={onTest} title="测试连接">
          🧪 测试
        </button>
        <button className="btn-icon-action" onClick={onEdit} title="编辑">
          ✏️ 编辑
        </button>
        <button className="btn-icon-action btn-danger" onClick={onDelete} title="删除">
          🗑️ 删除
        </button>
      </div>
    </div>
  )
}

// 机器人配置模态框
function BotConfigModal({
  platform,
  editingBot,
  onClose,
  onSave,
  onPlatformChange
}: {
  platform: keyof typeof platformInfo
  editingBot: BotConfig | null
  onClose: () => void
  onSave: (bot: BotConfig) => void
  onPlatformChange: (platform: keyof typeof platformInfo) => void
}) {
  const [name, setName] = useState(editingBot?.name || '')
  const [config, setConfig] = useState(editingBot?.config || {})

  const platformData = platformInfo[platform]

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!name.trim()) {
      alert('请输入机器人名称')
      return
    }

    // 验证必填字段
    const hasRequiredFields = platformData.fields.every(field =>
      config[field.key as keyof typeof config]
    )

    if (!hasRequiredFields) {
      alert('请填写所有必填字段')
      return
    }

    const bot: BotConfig = {
      id: editingBot?.id || Date.now().toString(),
      platform,
      name,
      enabled: editingBot?.enabled ?? true,
      config
    }

    onSave(bot)
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{editingBot ? '编辑' : '添加'}机器人</h3>
          <button className="btn-close-modal" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {!editingBot && (
              <div className="form-group">
                <label>选择平台</label>
                <div className="platform-selector">
                  {(Object.keys(platformInfo) as Array<keyof typeof platformInfo>).map(p => (
                    <button
                      key={p}
                      type="button"
                      className={`platform-btn ${platform === p ? 'active' : ''}`}
                      onClick={() => {
                        onPlatformChange(p)
                        setConfig({})
                      }}
                    >
                      <span className="platform-icon">{platformInfo[p].icon}</span>
                      <span>{platformInfo[p].name}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="form-group">
              <label>机器人名称 *</label>
              <input
                type="text"
                className="form-input"
                placeholder="例如：交易预警机器人"
                value={name}
                onChange={e => setName(e.target.value)}
                required
              />
            </div>

            {platformData.fields.map(field => (
              <div key={field.key} className="form-group">
                <label>{field.label} *</label>
                <input
                  type={field.type}
                  className="form-input"
                  placeholder={field.placeholder}
                  value={config[field.key as keyof typeof config] || ''}
                  onChange={e => setConfig({ ...config, [field.key]: e.target.value })}
                  required
                />
              </div>
            ))}

            <div className="form-help">
              <span>💡 不知道如何获取？</span>
              <a href={platformData.guide} target="_blank" rel="noopener noreferrer">
                查看{platformData.name}官方指南
              </a>
            </div>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-cancel" onClick={onClose}>
              取消
            </button>
            <button type="submit" className="btn-submit">
              {editingBot ? '保存' : '添加'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
