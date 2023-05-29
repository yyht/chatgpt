from typing import List

import torch
import torch.nn as nn
import torch.nn.functional as F

class MLPLayer(nn.Module):
    """Head for sentence-level classification tasks."""

    def __init__(self, hidden_size, dropout_prob):
        super().__init__()
        
        self.hidden_size = hidden_size
        self.dropout_prob = dropout_prob
        
        self.dense = nn.Linear(self.hidden_size, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_prob)
        
    def forward(self, x, **kwargs):
        x = self.dropout(x)
        x = self.dense(x)
        last_rep = torch.tanh(x)
        last_rep = self.dropout(last_rep)
        return last_rep



class RewardModel(nn.Module):

    def __init__(self, encoder):
        """
        init func.

        Args:
            encoder (transformers.AutoModel): backbone, 默认使用 ernie 3.0
        """
        super().__init__()
        self.encoder = encoder
        self.reward_layer = nn.Linear(768, 1)
        self.MLPLayer = MLPLayer(768, 0.1)

    def forward(
        self,
        input_ids: torch.tensor,
        token_type_ids: torch.tensor,
        attention_mask=None,
        pos_ids=None,
        return_mode='cls'
    ) -> torch.tensor:
        """
        forward 函数，返回每句话的得分值。

        Args:
            input_ids (torch.tensor): (batch, seq_len)
            token_type_ids (torch.tensor): (batch, seq_len)
            attention_mask (torch.tensor): (batch, seq_len)
            pos_ids (torch.tensor): (batch, seq_len)

        Returns:
            reward: (batch, 1)
        """
        model_outputs = self.encoder(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
            position_ids=pos_ids,
            attention_mask=attention_mask,
        )
        # (batch, hidden_size)
        
        hidden_states = model_outputs[0]
        if return_mode == 'cls':
            pooler_output = hidden_states[:, 0, :]
        else:
            pooler_output = hidden_states[:, 0, :]
        pooler_output = self.MLPLayer(pooler_output)
        reward = self.reward_layer(pooler_output)       # (batch, 1)
        return reward

