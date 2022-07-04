import { Title as BaseTitle, TitleProps as BaseTitleProps } from '../../ui-components/Typography';

type TitleProps = Omit<BaseTitleProps, 'align'>;

export const Title = (props: TitleProps) => <BaseTitle align="center" {...props} />;
