import React, { FC } from 'react'
import { Tag as TTag } from 'common/types/responses'
import color from 'color'
import Format from 'common/utils/format'
import { IonIcon } from '@ionic/react'
import { alarmOutline, lockClosed } from 'ionicons/icons'
import Tooltip from 'components/Tooltip'
import { getTagColor } from './Tag'
import OrganisationStore from 'common/stores/organisation-store'
import Utils from 'common/utils/utils'
import classNames from 'classnames'
import Icon from 'components/Icon'
type TagContent = {
  tag: Partial<TTag>
}
function escapeHTML(unsafe: string) {
  return unsafe.replace(
    /[\u0000-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u00FF]/g,
    (c) => `&#${`000${c.charCodeAt(0)}`.slice(-4)};`,
  )
}

const renderIcon = (tagType: string, tagColor: string, tagLabel: string) => {
  switch (tagType) {
    case 'STALE':
      return (
        <IonIcon
          className='ms-1'
          icon={alarmOutline}
          color={color(tagColor).darken(0.1).string()}
        />
      )
    case 'GITHUB':
      switch (tagLabel) {
        case 'PR Open':
          return <Icon name='pr-linked' />
        case 'PR Merged':
          return <Icon name='pr-merged' />
        case 'PR Closed':
          return <Icon name='pr-closed' />
        case 'PR Draft':
          return <Icon name='pr-draft' />
        case 'Issue Open':
          return <Icon name='issue-linked' />
        case 'Issue Closed':
          return <Icon name='issue-closed' />
        default:
          return
      }
    default:
      return (
        <IonIcon
          className='ms-1'
          icon={lockClosed}
          color={color(tagColor).darken(0.1).string()}
        />
      )
  }
}

const getTooltip = (tag: TTag | undefined) => {
  if (!tag) {
    return null
  }
  const stale_flags_limit_days = OrganisationStore.getProject(
    tag.project,
  )?.stale_flags_limit_days
  const disabled = Utils.tagDisabled(tag)
  const truncated = Format.truncateText(tag.label, 12)
  const isTruncated = truncated !== tag.label ? tag.label : null
  let tooltip = null
  switch (tag.type) {
    case 'STALE': {
      tooltip = `${
        disabled
          ? 'This feature is available with our <strong>Enterprise</strong> plan. '
          : ''
      }A feature is marked as stale if no changes have been made to it in any environment within ${stale_flags_limit_days} days. This is automatically applied and will be re-evaluated if you remove this tag unless you apply a permanent tag to the feature.`
      break
    }
    default:
      break
  }
  if (tag.is_permanent) {
    tooltip =
      'Features marked with this tag are not monitored for staleness and have deletion protection.'
  }
  const tagColor = getTagColor(tag, false)

  if (isTruncated) {
    return `<div>
        <span
          style='background-color: ${color(tagColor).fade(
            0.92,
          )}; border: 1px solid ${color(tagColor).fade(0.76)}; color: ${color(
      tagColor,
    ).darken(0.1)};'
          class="chip d-inline-block chip--xs me-1${
            disabled ? ' disabled' : ''
          }"
        >
          ${`${escapeHTML(tag.label)}`}
        </span>
          ${tooltip || ''}
      </div>`
  }
  return tooltip
}

const TagContent: FC<TagContent> = ({ tag }) => {
  const tagLabel = Format.truncateText(tag.label, 12)

  if (!tagLabel) {
    return null
  }

  const disabled = Utils.tagDisabled(tag)

  return (
    <Tooltip
      title={
        <span
          className={classNames('mr-1 flex-row align-items-center', {
            'opacity-50': disabled,
          })}
        >
          {tagLabel}
          {renderIcon(tag.type!, tag.color!, tag.label!)}
        </span>
      }
    >
      {getTooltip(tag)}
    </Tooltip>
  )
}

export default TagContent
